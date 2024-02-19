# -*- coding: utf-8 -*-


{
    'name': 'Product Auto Sku Code,rule,barcode by Category, Variants Supported',
    'summary': """
    Product Auto code. Auto sku code. Auto Default Attributes. Unique code, auto Tracking Type.
    Product rule by category.
    Product sort. Customize Sequence for category. like [raw-ipad-001],[raw-ipad-002]
    """,
    "version": '12.19.07.32',
    'category': 'Sales',
    'author': 'Sunpop.cn',
    'website': 'https://www.sunpop.cn',
    'license': 'AGPL-3',
    'sequence': 2,
    'installable': True,
    'auto_install': False,
    'application': True,
    'images': ['static/description/banner.png'],
    'description': """
        Best Product Auto code. Variants Supported. Auto Default Attributes. Unique code. Auto reference, unique reference.

        This module allows to associate a sequence to the product reference by category.
        The reference (default code) is unique (SQL constraint) and required.
        Support Product with or without Variants.
        1. Auto code for every Product and Product Variants.自动产品编码。
        2. Get different sequence for different category.不同产品目录生成不同产品编码。
        3. Auto Code for every product variants, like product20181130-001.自动多规格产品编码，形式为 主产品编码-001。
        4. Product code must be Unique.产品编码强制要求唯一。
        5. Quick default value for every category. 按指定目录生成指定产品默认值，。
        6. Multi language support.多语种支持。
        7. Auto barcode. 自动生成条码。
        8. Drag to sort the Product sku show order. 产品可拖拽设置排序
        9. Input category code to search category in many2one select list. 在产品目录下拉选择中输入唯一编码定位相应的产品目录
        10.Fix category complete name bug for i18n. 修正产品目录名称的算法，在多语言下不会只显示英文
        11.Add 'show_cat_name_short' in context to show short name of category. 在context中加入'show_cat_name_short'即可只显示目录短名称
    """,
    'pre_init_hook': 'pre_init_hook',
    'post_init_hook': 'post_init_hook',
    'depends': [
        'product',
        'stock',
        # 'sale',
        # 'purchase',
        # 'mrp',
                ],
    'data': [
        # 视图
        'views/product_category_views.xml',
        'views/product_template_views.xml',
        'views/product_product_views.xml',
        'data/product_sequence_data.xml',
        'data/product_category_data.xml',
    ],
    'demo': [
    ],
}
