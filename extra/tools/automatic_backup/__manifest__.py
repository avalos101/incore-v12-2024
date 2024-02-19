# -*- coding: utf-8 -*-
{
    'name': 'Automatic Backup (Dropbox, Google Drive, Amazon S3, SFTP)',
    'version': '1.5.4',
    'summary': 'Automatic Backups',
    'author': 'inCore',
    'description': """
    Automatic Backup
    """,
    'data': [
        'data/data.xml',
        'views/automatic_backup.xml',
        'security/security.xml'
    ],
    'depends': [
        'mail',
    ],
    'installable': True,
    'application': True,
}
