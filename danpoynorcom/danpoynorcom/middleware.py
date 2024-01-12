from django_minify_html.middleware import MinifyHtmlMiddleware


class ProjectMinifyHtmlMiddleware(MinifyHtmlMiddleware):
    minify_args = MinifyHtmlMiddleware.minify_args | {
        # Other options are documented here:
        # https://github.com/wilsonzlin/minify-html/blob/master/minhtml/src/main.rs
        # 'minify_css': True,  # For inline CSS
        # 'minify_js': True,  # Minify JS in <script> tags that have a valid or no type attribute value
        # 'minify_doctype': False,  # Broken
        'keep_comments': False,
        'keep_closing_tags': False,
        'keep_html_and_head_opening_tags': False,
        # 'allow_noncompliant_unquoted_attribute_values': True, # Broken
        # 'allow_optimal_entities': True, # Broken
        # 'allow_removing_spaces_between_attributes': True, # Broken
        # 'enable_possibly_noncompliant': True, # enable all of these at once - Broken
    }
