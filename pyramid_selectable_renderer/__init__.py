from zope.interface import provider
from zope.interface import implementer
from pyramid.renderers import RendererHelper
from .interfaces import ISelectableRendererSelector

__all__ = ["includeme", "selectable_renderer"]

_lookup_key = "__selectable"
def includeme(config):
    config.add_renderer(_lookup_key, SelectableRenderer)
    config.add_directive("add_selectable_renderer_selector", add_selectable_renderer_selector)

def add_selectable_renderer_selector(config, fun, name=""):
    fun = config.maybe_dotted(fun)
    config.registry.registerUtility(provider(ISelectableRendererSelector)(fun),
                                    ISelectableRendererSelector, 
                                    name=name)

def selectable_renderer(fmt, defaults=None):
    global _lookup_key
    lookup_key = StringLike(_lookup_key)
    lookup_key._format_string = fmt
    return lookup_key


class StringLike(str):
    pass

class SkinnyRendererHelper(RendererHelper):
    #@override
    def render(self, value, system_values, request=None):
        renderer = self.renderer
        return renderer(value, system_values)

class SelectableRenderer(object):
    def __init__(self, info):
        self.info = info
        ## xxx: this is hack.
        self.format_string = self.info.name._format_string
        self.renderers = {}

    def get_sub_renderer(self, path):
        renderer = self.renderers.get(path)
        if renderer:
            return renderer
        renderer = SkinnyRendererHelper(name=path,
                                        package=self.info.package,
                                        registry=self.info.registry)
        self.renderers[path] = renderer
        return renderer

    def __call__(self, value, system_values, request=None):
        request = request or system_values["request"]
        selector = request.registry.getUtility(ISelectableRendererSelector)
        renderer = self.get_sub_renderer(selector(self, value, system_values, request=request))
        renderer.render(value, system_values, request=request)
        return renderer.render(value, system_values, request=request)

## individual utility
@implementer(ISelectableRendererSelector)
class ByDomainMappingSelector(object):
    def __init__(self, mapping):
        self.mapping = mapping

    def lookup_mapped(self, domain_name):
        for k, lookup_key in self.mapping.iteritems():
            if k in domain_name:
                return lookup_key
        return self.mapping.get("default")

    def __call__(self, helper, value, system_values, request=None):
        assert request
        mapped = self.lookup_mapped(request.host)
        fmt = helper.format_string
        return fmt % dict(membership=mapped)
