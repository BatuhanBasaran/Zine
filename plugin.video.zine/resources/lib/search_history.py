# -*- coding: utf-8 -*-
import os, json, xbmcaddon, xbmcvfs
from xbmcvfs import translatePath

def _addon_id():
    return xbmcaddon.Addon().getAddonInfo('id')

def _hist_path(site_id: str):
    base = translatePath(f'special://profile/addon_data/{_addon_id()}/search_history')
    if not xbmcvfs.exists(base):
        xbmcvfs.mkdirs(base)
    # eine Datei je Site
    return os.path.join(base, f'{site_id}.json')

def load(site_id: str, max_items: int = 20):
    p = _hist_path(site_id)
    if not xbmcvfs.exists(p):
        return []
    try:
        f = xbmcvfs.File(p); data = f.read(); f.close()
        items = json.loads(data) or []
        return items[:max_items]
    except Exception:
        return []

def save(site_id: str, items):
    p = _hist_path(site_id)
    tmp = p + '.tmp'
    try:
        f = xbmcvfs.File(tmp, 'w')
        f.write(json.dumps(items, ensure_ascii=False))
        f.close()
        if xbmcvfs.exists(p): xbmcvfs.delete(p)
        xbmcvfs.rename(tmp, p)
    except Exception:
        try:
            if xbmcvfs.exists(tmp): xbmcvfs.delete(tmp)
        except Exception:
            pass

def add(site_id: str, query: str, max_items: int = 20):
    if not query: return
    q = query.strip()
    if not q: return
    items = load(site_id, max_items)
    items = [i for i in items if i.lower() != q.lower()]
    items.insert(0, q)
    save(site_id, items[:max_items])

def clear(site_id: str):
    save(site_id, [])
