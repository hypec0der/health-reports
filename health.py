

import requests
import argparse
import sys


who_api_request = "http://apps.who.int:80/gho/athena/api/{}/{}"


class QueryAction(argparse.Action):

    def __init__(self,option_strings,dest,help,nargs='?',choices=None):
        # Come destinazione prendi la chiave query 
        super().__init__(option_strings,dest='query',choices=choices,help=help,required=False,type=str)
        # Salva il nome della destinazione
        self.name = dest

    # Questo metodo converte direttamente la lista di codici in una stringa
    def __call__(self,parser,namespace,values,option_string=None):
        # Se query è nulla, ritorna un dizionario vuoto altrimenti ritorna il dizionario delle query
        query = (lambda query: query if query is not None else {})(vars(namespace).get('query'))
        # Aggiorna il dizionario con la nuova query formata dal nome e dal valore passato come argomento
        query.update({self.name: values})
        # Aggiorna il namespace
        setattr(namespace, 'query', query)


def main():
    # Creo il parser per gli argomenti a linea di comando
    parser = argparse.ArgumentParser(description='World Healt Organisation api query')
    # Creo un gruppo per i database
    database = parser.add_argument_group('Database selection')
    database.add_argument('--dimension',dest='dimension',default='',type=str,help='The dimension you wish to target')
    database.add_argument('--code',dest='codes',default='',type=str,help='The specific code(s) for which you wish to download data')
    # Creo gruppo per le query
    query = parser.add_argument_group('Query')
    query.add_argument('--format',dest='format',action=QueryAction,help='The output format you wish to use',choices=['xml','json','csv'])
    query.add_argument('--target',dest='target',action=QueryAction,help='Overides the target specifed in the DIMENSION and CODE components of the URL.')
    query.add_argument('--filter',dest='filter',action=QueryAction,help='Restricts the data returned by specifying filtering codes. The filter value is a semicolon separated list of tokens of the form DIMENSION:CODE.')
    query.add_argument('--profile',dest='profile',action=QueryAction,help='A modifier that allows you to specify different versions of the requested format')
    query.add_argument('--callback',dest='callback',action=QueryAction,help='When specifying a JSON format, adding the callback or jsonp parameter will wrap the returned javascript in the specified function')
    # vars return dictionary instead of NameSpace
    args = parser.parse_args()
    # Costruisco l'url per la richiesta alla API    
    url = who_api_request.format(args.dimension,args.codes)
    # Effettuo la richiesta
    req = requests.request('GET',url,params=args.query)
    # Verifico che la richiesta sia andata a buon fine
    assert req.status_code == requests.codes.ok, ConnectionError('Request error')
    # Stampo il risultato
    sys.stdout.write(req.text)
    # Flush
    sys.stdout.flush() 
        


if __name__ == '__main__':
    main()
