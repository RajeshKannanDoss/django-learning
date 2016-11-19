# -*- coding: utf-8 -*-


def url_to_id(link, model):
    return model.objects.get(shortcut=link)
