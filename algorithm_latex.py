def create_topology(linestrings, valid_nodes):
  sublinks = []
  for ls in linestrings: # linestrings: List of LineStrings
    source = ls[0] # LineStrings are assummed array-like
    for target in ls[1:]:
      if target not in valid_nodes: # valid_nodes: Nodes visited more than once
        continue
      sublink = split(ls, source, target) # split: Creates LineString from two nodes
      sublinks.append(sublink) # sublinks: List of decomposed LineStrings
      source = target
  return sublinks