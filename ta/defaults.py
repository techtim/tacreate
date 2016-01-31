from mezzanine.conf import register_setting

register_setting(
    name="TEMPLATE_ACCESSIBLE_SETTINGS",
    append=True,
    default=("PROJECTS_PER_PAGE",
    		"GOOGLE_ANALYTICS_ID",
    		"SOCIAL_LINK_FACEBOOK",
    		"RICHTEXT_FILTER_LEVEL",
             ),
    )

register_setting(
    name="PROJECTS_PER_PAGE",
    label="PROJECTS per page",
    description="The number of PROJECTS to show per author page.",
    editable=True,
    default=6,
)

register_setting(
    name="GOOGLE_ANALYTICS_ID",
    default="a49747697w81574826p84448278",
)

register_setting(
    name="SOCIAL_LINK_FACEBOOK",
    label="Facebook link",
    description= "If present a Facebook icon linking here will be in the "
        "header.",
    editable=True,
    default="https://facebook.com/tacreate",
)

register_setting(
    name="RICHTEXT_FILTER_LEVEL",
	default=3,
)