

sid_templates = {

    # type asset
    'asset__file':            '{project}/{type:a}/{assettype}/{asset}/{task}/{version}/{state}/{ext:scenes}',
    'asset__movie_file':      '{project}/{type:a}/{assettype}/{asset}/{task}/{version}/{state}/{ext:movies}',
    'asset__cache_file':      '{project}/{type:a}/{assettype}/{asset}/{task}/{version}/{state}/{ext:caches}',

    'asset__state':           '{project}/{type:a}/{assettype}/{asset}/{task}/{version}/{state}',  # extrapolated

    'asset':                  '{project}/{type:a}',

    # type shot
    'shot__file':             '{project}/{type:s}/{sequence}/{shot}/{task}/{version}/{state}/{ext:scenes}',
    'shot__movie_file':       '{project}/{type:s}/{sequence}/{shot}/{task}/{version}/{state}/{ext:movies}',
    'shot__cache_file':       '{project}/{type:s}/{sequence}/{shot}/{task}/{version}/{state}/{ext:caches}',
    'shot__cache_node_file':  '{project}/{type:s}/{sequence}/{shot}/{task}/{version}/{state}/{node}/{ext:caches}',
    'shot__cache_node':       '{project}/{type:s}/{sequence}/{shot}/{task}/{version}/{state}/{node}',

    'shot__state':            '{project}/{type:s}/{sequence}/{shot}/{task}/{version}/{state}',  # extrapolated

    'shot':                   '{project}/{type:s}',

    # type project
    'project':                '{project}',

}


if __name__ == "__main__":

    for k, v in sid_templates.items():
        print(f'{k}: {v}')

