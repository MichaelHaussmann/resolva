
# basic pattern
sid_templates_pre = {

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

# After adding some expressions
sid_templates = {
    "asset__file": r"{project:(hamlet|\*|\>)}/{type:(a|\*|\>)}/{assettype:(char|location|prop|fx|\*|\>)}/{asset}/{task:(art|model|surface|rig|\*|\>)}/{version:(v\d\d\d|\*|\>)}/{state:(w|p|\*|\>)}/{ext:(ma|mb|hip|blend|hou|psd|nk|maya|\*|\>)}",
    "asset__movie_file": r"{project:(hamlet|\*|\>)}/{type:(a|\*|\>)}/{assettype:(char|location|prop|fx|\*|\>)}/{asset}/{task:(art|model|surface|rig|\*|\>)}/{version:(v\d\d\d|\*|\>)}/{state:(w|p|\*|\>)}/{ext:(mp4|mov|avi|movie|\*|\>)}",
    "asset__cache_file": r"{project:(hamlet|\*|\>)}/{type:(a|\*|\>)}/{assettype:(char|location|prop|fx|\*|\>)}/{asset}/{task:(art|model|surface|rig|\*|\>)}/{version:(v\d\d\d|\*|\>)}/{state:(w|p|\*|\>)}/{ext:(abc|json|fur|grm|vdb|cache|\*|\>)}",
    "asset__state": r"{project:(hamlet|\*|\>)}/{type:(a|\*|\>)}/{assettype:(char|location|prop|fx|\*|\>)}/{asset}/{task:(art|model|surface|rig|\*|\>)}/{version:(v\d\d\d|\*|\>)}/{state:(w|p|\*|\>)}",
    "asset__version": r"{project:(hamlet|\*|\>)}/{type:(a|\*|\>)}/{assettype:(char|location|prop|fx|\*|\>)}/{asset}/{task:(art|model|surface|rig|\*|\>)}/{version:(v\d\d\d|\*|\>)}",
    "asset__task": r"{project:(hamlet|\*|\>)}/{type:(a|\*|\>)}/{assettype:(char|location|prop|fx|\*|\>)}/{asset}/{task:(art|model|surface|rig|\*|\>)}",
    "asset__asset": r"{project:(hamlet|\*|\>)}/{type:(a|\*|\>)}/{assettype:(char|location|prop|fx|\*|\>)}/{asset}",
    "asset__assettype": r"{project:(hamlet|\*|\>)}/{type:(a|\*|\>)}/{assettype:(char|location|prop|fx|\*|\>)}",
    "asset": r"{project:(hamlet|\*|\>)}/{type:(a|\*|\>)}",
    "shot__file": r"{project:(hamlet|\*|\>)}/{type:(s|\*|\>)}/{sequence:(sq\d\d\d|\*|\>)}/{shot:(sh\d\d\d\d|\*|\>)}/{task:(board|layout|anim|fx|render|comp|\*|\>)}/{version:(v\d\d\d|\*|\>)}/{state:(w|p|\*|\>)}/{ext:(ma|mb|hip|blend|hou|psd|nk|maya|\*|\>)}",
    "shot__movie_file": r"{project:(hamlet|\*|\>)}/{type:(s|\*|\>)}/{sequence:(sq\d\d\d|\*|\>)}/{shot:(sh\d\d\d\d|\*|\>)}/{task:(board|layout|anim|fx|render|comp|\*|\>)}/{version:(v\d\d\d|\*|\>)}/{state:(w|p|\*|\>)}/{ext:(mp4|mov|avi|movie|\*|\>)}",
    #"shot__cache_file": r"{project:(hamlet|\*|\>)}/{type:(s|\*|\>)}/{sequence:(sq\d\d\d|\*|\>)}/{shot:(sh\d\d\d\d|\*|\>)}/{task:(board|layout|anim|fx|render|comp|\*|\>)}/{version:(v\d\d\d|\*|\>)}/{state:(w|p|\*|\>)}/{ext:(abc|json|fur|grm|vdb|cache|\*|\>)}",
    "shot__cache_node_file": r"{project:(hamlet|\*|\>)}/{type:(s|\*|\>)}/{sequence:(sq\d\d\d|\*|\>)}/{shot:(sh\d\d\d\d|\*|\>)}/{task:(board|layout|anim|fx|render|comp|\*|\>)}/{version:(v\d\d\d|\*|\>)}/{state:(w|p|\*|\>)}[/{node}]/{ext:(abc|json|fur|grm|vdb|cache|\*|\>)}",
    "shot__cache_node": r"{project:(hamlet|\*|\>)}/{type:(s|\*|\>)}/{sequence:(sq\d\d\d|\*|\>)}/{shot:(sh\d\d\d\d|\*|\>)}/{task:(board|layout|anim|fx|render|comp|\*|\>)}/{version:(v\d\d\d|\*|\>)}/{state:(w|p|\*|\>)}/{node}",
    "shot__state": r"{project:(hamlet|\*|\>)}/{type:(s|\*|\>)}/{sequence:(sq\d\d\d|\*|\>)}/{shot:(sh\d\d\d\d|\*|\>)}/{task:(board|layout|anim|fx|render|comp|\*|\>)}/{version:(v\d\d\d|\*|\>)}/{state:(w|p|\*|\>)}",
    "shot__version": r"{project:(hamlet|\*|\>)}/{type:(s|\*|\>)}/{sequence:(sq\d\d\d|\*|\>)}/{shot:(sh\d\d\d\d|\*|\>)}/{task:(board|layout|anim|fx|render|comp|\*|\>)}/{version:(v\d\d\d|\*|\>)}",
    "shot__task": r"{project:(hamlet|\*|\>)}/{type:(s|\*|\>)}/{sequence:(sq\d\d\d|\*|\>)}/{shot:(sh\d\d\d\d|\*|\>)}/{task:(board|layout|anim|fx|render|comp|\*|\>)}",
    "shot__shot": r"{project:(hamlet|\*|\>)}/{type:(s|\*|\>)}/{sequence:(sq\d\d\d|\*|\>)}/{shot:(sh\d\d\d\d|\*|\>)}",
    "shot__sequence": r"{project:(hamlet|\*|\>)}/{type:(s|\*|\>)}/{sequence:(sq\d\d\d|\*|\>)}",
    "shot": r"{project:(hamlet|\*|\>)}/{type:(s|\*|\>)}",
    "project": r"{project:(hamlet|\*|\>)}",
    # "something": r"{project:(hamlet|\*|\>)}/{type:(s|\*|\>)}/{project}",  # duplicate placeholder "project"
}


if __name__ == "__main__":

    for k, v in sid_templates.items():
        print(f'{k}: {v}')

