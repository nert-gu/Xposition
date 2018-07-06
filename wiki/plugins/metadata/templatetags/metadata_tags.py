from django import template
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q
from django.utils.safestring import mark_safe
from django_tables2 import RequestConfig
from bitfield import BitField
from wiki.models import Article, ArticleRevision
from wiki.models.pluginbase import RevisionPlugin, RevisionPluginRevision
from wiki.plugins.metadata.models import MetadataRevision, SimpleMetadata, Supersense, Construal, Language, Adposition, Usage, PTokenAnnotation, deepest_instance
from wiki.plugins.metadata.tables import PTokenAnnotationTable
from wiki.plugins.categories.models import Category

register = template.Library()

@register.simple_tag(takes_context=True)
def metadata_display(context):
    if 'article' not in context:
        return ''

    article = context['article']
    c = article.current_revision
    if hasattr(c, 'metadata_revision'):
        meta = deepest_instance(c.metadata_revision)
    else:
        articleplugins = [deepest_instance(z) for z in article.articleplugin_set.all()]
        meta = [z for z in articleplugins if isinstance(z, SimpleMetadata)]   # not Metadata, because that will have an article_revision pointer and be handled above
        assert 0<=len(meta)<=1
        if meta:
            meta = meta[0]
        else:
            return

    #meta = deepest_instance(metadata)
    #if hasattr(meta, 'current_revision'):
    #    meta = deepest_instance(meta.current_revision)
    generic_flds = MetadataRevision._meta.get_fields() + SimpleMetadata._meta.get_fields()
    display = '<h4 id="metadata">Metadata'
    if hasattr(meta, 'editurl'):
        editurl = meta.editurl(context['urlpath'])
        display += ' <a href="' + editurl + '" style="float: right;"><i class="fa fa-edit" alt="edit metadata"></i></a>'
    display += '</h4>\n<table class="metadata">\n'
    for fld in meta._meta.get_fields(include_hidden=False):
        if fld.name=='description' or fld not in generic_flds and not fld.name.endswith('_ptr'):
            display += f'    <tr><th style="padding: 10px;">{fld.name}</th><td>'
            v = getattr(meta, fld.name)
            if hasattr(v, 'html'):
                display += v.html()
            elif hasattr(fld, 'choices') and fld.choices:
                choices = dict(fld.choices)
                if v is not None:   # if None, display nothing
                    v = str(choices[int(v)])
                    display += str(v)
            elif isinstance(fld, BitField):
                display += ', '.join(case for case,allowed in v if allowed)
            elif fld.name=='description' and hasattr(meta, 'descriptionhtml'):
                display += meta.descriptionhtml()
            else:
                display += str(v)
            display += '</td></tr>\n'
    display += '</table>'
    display += '<!--'+str(meta)+'-->'
    return mark_safe(display)


@register.simple_tag(takes_context=True)
def langs_display(context):
    """Display a list of languages recorded in the database."""
    if 'article' not in context:
        return ''

    article = context['article']
    s = ''
    for lang in Language.with_nav_links().order_by('name'):
        # issue #9: get rid of deleted articles in lists
        if lang.article.current_revision.deleted:
            continue
        langart = lang.article
        s += '<li'
        if context['article']==langart \
            or (hasattr(article, 'metadata') and getattr(context['article'].metadata, 'language', None)==lang) \
            or (hasattr(article.current_revision, 'metadata_revision') and getattr(deepest_instance(context['article'].current_revision.metadata_revision), 'lang', None)==lang):
            s += ' class="active"'
        s += '><a href="' + langart.get_absolute_url() + '">' + lang.name + '</a></li>"'
    return mark_safe(s)

@register.simple_tag(takes_context=True)
def adpositions_for_lang(context):
    article = context['article']
    # issue #9: get rid of deleted articles in lists
    a = Adposition.objects.filter(current_revision__metadatarevision__adpositionrevision__lang__article=article,
        current_revision__metadatarevision__article_revision__deleted=False)
    return a

@register.simple_tag(takes_context=True)
def usages_for_lang(context):
    article = context['article']
    # issue #9: get rid of deleted articles in lists
    u = Usage.objects.filter(current_revision__metadatarevision__usagerevision__adposition__current_revision__metadatarevision__adpositionrevision__lang__article=article,
        current_revision__metadatarevision__article_revision__deleted=False)
    return u

@register.simple_tag(takes_context=True)
def usages_for_adp(context):
    article = context['article']
    # issue #9: get rid of deleted articles in lists
    u = Usage.objects.filter(current_revision__metadatarevision__usagerevision__adposition__article=article,
        current_revision__metadatarevision__article_revision__deleted=False)
    return u

@register.simple_tag(takes_context=True)
def usages_for_construal(context):
    article = context['article']
    
    
    """ # using related_name sounds nice in principle, but actually looks pretty nasty
    construal = deepest_instance(article.articleplugin_set.first())
    urs = construal.usages.filter(article_revision__deleted=False)    # UsageRevision instances
    u = [ur.plugin_set.first() for ur in urs] # Usage instances
    """
    
    # issue #9: get rid of deleted articles in lists
    u = Usage.objects.filter(current_revision__metadatarevision__usagerevision__construal__article=article, 
        current_revision__metadatarevision__usagerevision__article_revision__deleted=False)
    return u

def paginate(items, context):
    request = context['request']
    """"
    perpage = request.GET.get('perpage', 25)
    if int(perpage)<0: perpage = 10000 # practically no limit
    page = request.GET.get('page', 1)
    context['page'] = page
    context['perpage'] = perpage
    paginator = Paginator(items, perpage)
    context['pag'] = paginator
    """
    table = PTokenAnnotationTable(items)
    RequestConfig(request, paginate={'per_page': 25}).configure(table)
    context['tokstable'] = table
    return table

@register.simple_tag(takes_context=True)
def tokens_for_adposition(context):
    article = context['article']
    # issue #9: get rid of deleted articles in lists
    t = PTokenAnnotation.objects.filter(adposition__article=article).order_by('sentence__sent_id')
    return paginate(t, context)

@register.simple_tag(takes_context=True)
def tokens_for_construal(context):
    article = context['article']
    # issue #9: get rid of deleted articles in lists
    t = PTokenAnnotation.objects.filter(construal__article=article).order_by('sentence__sent_id')
    return paginate(t, context)

@register.simple_tag(takes_context=True)
def tokens_for_supersense(context):
    article = context['article']
    # issue #9: get rid of deleted articles in lists
    t = PTokenAnnotation.objects.filter(Q(construal__role__article=article) | Q(construal__function__article=article)).order_by('sentence__sent_id')
    return paginate(t, context)

@register.simple_tag(takes_context=True)
def tokens_for_usage(context):
    article = context['article']
    # issue #9: get rid of deleted articles in lists
    t = PTokenAnnotation.objects.filter(usage__article=article).order_by('sentence__sent_id')
    return paginate(t, context)

@register.simple_tag(takes_context=False)
def split(s):
    return s.split(' ')

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

@register.simple_tag(takes_context=False)
def truncate_contents_after_colon(s):
    i = s.index('>')+1
    j = s.index('</', i)
    c = s.index(':', i)
    return s[:c] + s[j:]

@register.simple_tag(takes_context=False)
def other_p_tokens_in_sentence(pt):
    others = pt.sentence.ptokenannotation_set.exclude(pk=pt.pk)
    result = {}
    for opt in others:
        assert opt.main_subtoken_indices[0] not in result
        assert opt.main_subtoken_indices[-1] not in result
        result[opt.main_subtoken_indices[0]] = opt # open the link
        result[opt.main_subtoken_indices[-1]] = opt    # close the link
    return result

def _category_subtree(c, recursive=False):
    ss = c.supersense.all()[0]
    a = ss.article
    #s = '<li><a href="{url}">{rev}</a>'.format(url=a.get_absolute_url(), rev=a.current_revision.title)
    s = f'<li class="clt">{ss.metadata.html()}' if not recursive else f'<li>{ss.metadata.html()}'
    # number of construals for the supersense
    nAsRole = len(ss.rfs_with_role.all())
    nAsFunction = len(ss.rfs_with_function.all())
    s += ' <small style="font-size: 50%;">{}<span style="color: #999;" class="construal-arrow">&#x219d;</span>{}</small>'.format(nAsRole, nAsFunction)
    #print(s)
    # issue #9: get rid of deleted articles in lists
    children = c.children.all() #.filter(current_revision__metadatarevision__article_revision__deleted=False)
    #print(children)
    if len(children):
        s += '\n<ul>'
        for child in children:
            s += _category_subtree(child, recursive=True)
        s += '\n</ul>'
    s += '</li>'
    return s

@register.simple_tag(takes_context=True)
def supersenses_display(context, top):
    """Display a list of supersenses recorded in the database."""
    try:
        t = Supersense.objects.get(current_revision__metadatarevision__name=top)
		# address issue #33
        #t = t.filter(current_revision__metadatarevision__article_revision__deleted=False)
        return mark_safe(_category_subtree(t.category))
    except Exception as ex:
        return 'NOT FOUND'

@register.simple_tag(takes_context=True)
def construals_display(context, role=None, function=None, order_by='role' or 'function'):
    """Display a list of supersenses recorded in the database."""
    order_by2 = 'role' if order_by=='function' else 'function'
    s = ''
    cc = Construal.objects.all()
    if role is not None:
        cc = cc.filter(role__current_revision__metadatarevision__name=role)
    if function is not None:
        cc = cc.filter(function__current_revision__metadatarevision__name=function)
    # issue #9: get rid of deleted articles in lists
    cc = cc.filter(article__current_revision__deleted=False)
    for c in cc.order_by(order_by+'__current_revision__metadatarevision__name',
                         order_by2+'__current_revision__metadatarevision__name'):
        #a = c.article
        #s += '<li><a href="{url}">{rev}</a></li>\n'.format(url=a.get_absolute_url(), rev=a.current_revision.title)
        s += f'<li>{c.html()}</li>\n'
    return mark_safe(s)
