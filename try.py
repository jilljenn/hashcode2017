from collections import namedtuple, Counter
Request = namedtuple('Request', 'video endpoint nb')

with open('kittens.in') as f:
    lines = []
    for line in f:
        lines.append(line)
    V, E, R, C, X = map(int, lines[0].split())
    size = list(map(int, lines[1].split()))
    to_data = []
    to_cache = []
    c = 2
    for endpoint in range(E):
        dist, nb_caches = map(int, lines[c].split())
        c += 1
        to_data.append(dist)  # Distance endpoint-datacenter
        to_cache.append({})
        for cache in range(nb_caches):
            i_cache, dist = map(int, lines[c].split())
            c += 1
            to_cache[endpoint][i_cache] = dist
    requests = []
    for request in range(R):
        i_video, i_endpoint, nb_requests = map(int, lines[c].split())
        c += 1
        requests.append(Request(video=i_video, endpoint=i_endpoint, nb=nb_requests))

score = Counter()
for r in requests:
    for i_cache in to_cache[r.endpoint]:
        score[(r.video, i_cache)] += (to_data[r.endpoint] - to_cache[r.endpoint][i_cache]) * r.nb
contained = [[] for _ in range(C)]
done = [False] * V
for (i_video, i_cache), _ in score.most_common():
    if not done[i_video] and sum(size[v] for v in contained[i_cache]) + size[i_video] <= X:
        contained[i_cache].append(i_video)
        done[i_video] = True
for (i_video, i_cache), _ in score.most_common():
    if not i_video in contained[i_cache] and sum(size[v] for v in contained[i_cache]) + size[i_video] <= X:
        contained[i_cache].append(i_video)
print(C)
for i_cache in range(C):
    print(i_cache, ' '.join(map(str, contained[i_cache])))
