from raptus.article.core.interfaces import IArticle


class IConfigurableArticle(IArticle):
    """Marker interface for Articles with context-aware component
    configuration.
    """
