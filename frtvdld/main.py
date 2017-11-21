#!/usr/bin/env python2
# -*- coding:Utf-8 -*-

#
# Infos
#

__author__ = "Chaoswizard"
__license__ = "GPL 2"
__version__ = "0.9.4"
__url__ = "http://code.google.com/p/tvdownloader/"

#
# Modules
#

import requests
import argparse
import logging
import platform
import re
import sys

from ColorFormatter import ColorFormatter
from francetv.FranceTvDownloader import FranceTvDownloader
from Navigateur import FakeAgent

#
# Main
#

REG_EXP = 'www.france.tv/(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'

def ExtractUrl(url):
    page = requests.get(url)

    # print "page.content", page.content
    index = page.content.find("la sélection")

    urls = re.findall(REG_EXP, page.content[index:])
    target =urls[0].replace("www.","https://")

    print "Target URl:", target
    return target


if (__name__ == "__main__"):

    # Arguments de la ligne de commande
    usage = "pluzzdl [options] urlEmission"
    parser = argparse.ArgumentParser(usage=usage, description="Télécharge les émissions de Pluzz")
    parser.add_argument("-b", "--progressbar", action="store_true", default=False,
                        help='affiche la progression du téléchargement')
    parser.add_argument("-v", "--verbose", action="store_true", default=False,
                        help='affiche les informations de debugage')
    parser.add_argument("-t", "--soustitres", action="store_true", default=False,
                        help='récupère le fichier de sous-titres de la vidéo (si disponible)')

    parser.add_argument("-o", "--outDir", action="store", default=None, help='output folder (default .)')
    # parser.add_argument("-x", "--extractedUrl", action="store_true", default=False, help='extract Selection URL (france.tv)')

    parser.add_argument("--nocolor", action='store_true', default=False, help='désactive la couleur dans le terminal')
    parser.add_argument("--version", action='version', version="pluzzdl %s" % (__version__))
    parser.add_argument("urlEmission", action="store", help="URL de l'émission Pluzz a charger")
    args = parser.parse_args()

    # Mise en place du logger
    logger = logging.getLogger("frtvdld")
    console = logging.StreamHandler(sys.stdout)
    if (args.verbose):
        logger.setLevel(logging.DEBUG)
        console.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)
        console.setLevel(logging.INFO)
    console.setFormatter(ColorFormatter(not args.nocolor))
    logger.addHandler(console)

    # Affiche des infos sur le systeme
    logger.debug("frtvdld %s with Python %s (%s)" % (__version__, platform.python_version(), platform.machine()))
    logger.debug("OS : %s %s" % (platform.system(), platform.version()))

    # if (re.match("https://www.france.tv/[^\.]+?\.html", args.urlEmission) is None):
    #     logger.error("L'URL \"%s\" n'est pas valide" % (args.urlEmission))
    #     sys.exit(-1)

    # # Verification du proxy
    # if (args.proxy is not None):
    #     if (args.sock):
    #         if (re.match('[0-9]+(?:\.[0-9]+){3}:[0-9]+', args.proxy) is None):
    #             logger.error("Le proxy SOCK \"%s\" n'est pas valide" % (args.proxy))
    #             sys.exit(-1)
    #     else:
    #         if (re.match("http://[^:]+?:\d+", args.proxy) is None):
    #             logger.error("Le proxy HTML \"%s\" n'est pas valide" % (args.proxy))
    #             sys.exit(-1)

    # Fonction d'affichage de l'avancement du téléchargement
    if (args.progressbar):
        progressFnct = lambda x: logger.info("Avancement : %3d %%" % (x))
    else:
        progressFnct = lambda x: None

    # # extract target url from Emission page
    # if (args.extractedUrl):
    #     target = ExtractUrl(args.urlEmission)
    # else:
    #     target = args.urlEmission

    # logger.info( args.urlEmission )
    # logger.info( args.proxy)
    # logger.info(  args.sock )
    # Telechargement de la video
    # PluzzDL(url=target,
    #         proxy=args.proxy,
    #         proxySock=args.sock,
    #         sousTitres=args.soustitres,
    #         progressFnct=progressFnct,
    #         outDir=args.outDir)

    FranceTvDownloader(url=args.urlEmission,
            fakeAgent=FakeAgent(),
            sousTitres=args.soustitres,
            progressFnct=progressFnct,
            outDir=args.outDir)

    # ArteDownloader(url=target,
    #         proxy=args.proxy,
    #         proxySock=args.sock,
    #         sousTitres=args.soustitres,
    #         progressFnct=progressFnct,
    #         outDir=args.outDir)