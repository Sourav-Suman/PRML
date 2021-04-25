#!/usr/bin/env python
# coding: utf-8

# In[2]:


def get_matched_pairs(true_scenes, scenes):

    def get_max_intersection(intersections):
        mx = -1 #stores maximum intersection value
        r = -1 #stores scene with maximum intersection
        for val in intersections.keys():
            if intersections[val]>mx:
                mx = intersections[val]
                r = val
            elif intersections[val] == mx:
                r = -1 #if equal intersection then ignore
        return r

    matched_pairs = list()
#     get intersection of scenes in true scenes

    strt = 0 #start of scene
    scene_map_truescene = dict() #final dict for scenes
    for i, e in enumerate(scenes):
        e_te = dict() #temporary dict for intersections
        idx = 0
        for j,te in enumerate(true_scenes):
            if te<strt:
                continue
            elif te>e:
                break
            else:
                e_te[j]=te-strt #get num of sentences of an scene e in true scene te
                strt = te #define the new starting point as the ending point of previous true scene
                idx = j+1 #for final intersection
        e_te[idx]=e-strt
        scene_map_truescene[i] = get_max_intersection(e_te)


#     get intersection of true scenes in scenes

    strt = 0 #start of scene
    truescene_map_scene = dict() #final dict for scenes
    for i, te in enumerate(true_scenes):
        te_e = dict() #temporary dict for intersections
        idx = 0
        for j,e in enumerate(scenes):
            if e<strt:
                continue
            elif e>te:
                break
            else:
                te_e[j]=e-strt #get num of sentences of an scene e in true scene te
                strt = e #define the new starting point as the ending point of previous true scene
                idx = j+1 #for final intersection
        te_e[idx]=te-strt
        truescene_map_scene[i] = get_max_intersection(te_e)

#     print("1 ",scene_map_truescene,"\n2: ", truescene_map_scene)
#         check for intersection in both mappings
    for key in scene_map_truescene.keys():
        te_key = scene_map_truescene[key] #get the matched true scene for the scene "key"
        if te_key in truescene_map_scene:
            if truescene_map_scene[te_key] == key:  #check if the true scene is also matched to the same scene
                matched_pairs.append((key, te_key))
#     print("\n",matched_pairs)
    return matched_pairs



# In[13]:


def IoU(true_scenes, scenes, total_sentences):
    matched_pairs = get_matched_pairs(true_scenes, scenes)
    total_ev_sentences = total_tev_sentences = set(range(total_sentences))
    IoU = list()
    avgIoU = 0
    for (ev, tev) in matched_pairs:
#         get list of sentences for an scene
        if ev == 0:
            ev_list = set(range(scenes[ev]))
        else :
            ev_list = set(range(scenes[ev-1], scenes[ev]))
        if tev == 0:
            tev_list = set(range(true_scenes[tev]))
        else :
            tev_list = set(range(true_scenes[tev-1], true_scenes[tev]))
#           find intersection between sentences in generated scene and true scene
        inter = min(len(ev_list.intersection(tev_list)), len(tev_list.intersection(ev_list)))
#           find union between sentences in generated scene and true scene
        union = len(ev_list.union(tev_list))
#           find left out sentences after generated scene and true scene
        total_ev_sentences = total_ev_sentences.difference(ev_list)
        total_tev_sentences = total_tev_sentences.difference(tev_list)
        IoU.append(inter/union)
    if len(IoU) == 0:
        avgIoU = 0
    else:
        avgIoU = sum(IoU)/(len(IoU))
    return (avgIoU, (len(total_ev_sentences.intersection(total_tev_sentences))/total_sentences))
