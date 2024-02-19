# -*- coding: utf-8 -*-
# Part of inCore. See LICENSE file for full copyright and licensing details.

import incore

# ----------------------------------------------------------
# Monkey patch release to set the edition as 'enterprise'
# ----------------------------------------------------------
incore.release.version_info = incore.release.version_info[:5] + ('e',)
if '+e' not in incore.release.version:     # not already patched by packaging
    incore.release.version = '{0}+e{1}{2}'.format(*incore.release.version.partition('-'))

incore.service.common.RPC_VERSION_1.update(
    server_version=incore.release.version,
    server_version_info=incore.release.version_info)
