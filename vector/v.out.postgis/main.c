/***************************************************************
 *
 * MODULE:       v.out.postgis
 *
 * AUTHOR(S):    Martin Landa <landa.martin gmail.com>
 *
 * PURPOSE:      Converts GRASS vector map layer to PostGIS
 *
 * COPYRIGHT:    (C) 2012 by Martin Landa, and the GRASS Development Team
 *
 *               This program is free software under the GNU General
 *               Public License (>=v2). Read the file COPYING that
 *               comes with GRASS for details.
 *
 **************************************************************/

#include <stdlib.h>

#include <grass/gis.h>
#include <grass/glocale.h>

#include "local_proto.h"

int main(int argc, char *argv[])
{
    struct GModule *module;
    struct params params;
    struct flags flags;
    
    int ret, field;
    char *schema, *olayer, *pg_file;
    struct Map_info In, Out;
    
    G_gisinit(argv[0]);

    module = G_define_module();
    G_add_keyword(_("vector"));
    G_add_keyword(_("export"));
    G_add_keyword(_("PostGIS"));
    G_add_keyword(_("simple features"));
    G_add_keyword(_("topology"));

    module->description =
        _("Exports a vector map layer to PostGIS feature table.");
    module->overwrite = TRUE;
    
    define_options(&params, &flags);
    
    if (G_parser(argc, argv))
        exit(EXIT_FAILURE);

    /* if olayer not given, use input as the name */
    schema = NULL;
    if (!params.olayer->answer) {
        char name[GNAME_MAX], mapset[GMAPSET_MAX];
        
        /* check for fully qualified name */
        if (G_name_is_fully_qualified(params.input->answer,
                                      name, mapset))
            olayer = G_store(name);
        else
            olayer = G_store(params.input->answer);
        G_debug(1, "olayer=%s", olayer);
    }
    else {
        /* check for schema */
        char **tokens;

        tokens = G_tokenize(params.olayer->answer, ".");
        if (G_number_of_tokens(tokens) == 2) {
            schema = G_store(tokens[0]);
            olayer = G_store(tokens[1]);
        }
        else {
            olayer = G_store(params.olayer->answer);
        }
        
        G_free_tokens(tokens);
    }
    
    /* if schema not defined, use 'public' */
    if (!schema)
        schema = "public";
    G_debug(1, "Database schema: %s", schema);
        
    /* open input for reading */
    ret = Vect_open_old2(&In, params.input->answer, "", params.layer->answer);
    if (ret == -1)
        G_fatal_error(_("Unable to open vector map <%s>"),
                      params.input->answer);
    Vect_set_error_handler_io(&In, &Out);
    if (ret < 2) 
        G_warning(_("Unable to open vector map <%s> on topological level"),
                  params.input->answer);
    
    /* create output for writing */
    pg_file = create_pgfile(params.dsn->answer, schema, params.olink->answer,
                            params.opts->answers, flags.topo->answer ? TRUE : FALSE);
    
    if (-1 == Vect_open_new(&Out, olayer, Vect_is_3d(&In)))
        G_fatal_error(_("Unable to create PostGIS layer <%s>"),
                      olayer);
    
    /* define attributes */
    field = Vect_get_field_number(&In, params.layer->answer);
    if (!flags.table->answer)
        Vect_copy_map_dblinks(&In, &Out, TRUE);

    /* create PostGIS layer */
    create_table(&In, &Out);
    
    if (flags.topo->answer) 
        Vect_build_partial(&Out, GV_BUILD_NONE); /* upgrade level to 2 */
    
    /* copy vector features */
    if (Vect_copy_map_lines_field(&In, field, &Out) != 0)
        G_fatal_error(_("Copying features failed"));
    
    Vect_close(&In);
    
    if (Vect_build(&Out) != 1)
        G_fatal_error(_("Building %s topology failed"),
                      flags.topo->answer ? "PostGIS" : "pseudo");

    G_done_msg(_("Feature table <%s> created in database <%s>."),
               Vect_get_finfo_layer_name(&Out), Vect_get_finfo_dsn_name(&Out));
    
    Vect_close(&Out);

    /* remove PG file */
    G_remove("", pg_file);
    
    exit(EXIT_SUCCESS);
}
