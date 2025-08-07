#!/usr/bin/env -S uv run --script
#
# EXpkg - A simple yet quite powerful external packages manager
# Copyright (C) 2025 Maël GUERIN
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>. """
#
# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "nvchecker",
#     "wget",
# ]
# ///

import os, sys, subprocess, tempfile, argparse
import tomllib, json
import wget

parser = argparse.ArgumentParser(
    prog='expkg',
    description='A simple Python tool to manage your external packages'
)

parser.add_argument('--config', type=str, default=os.environ['HOME'] + '/.config/expkg/expkg.toml')


def parse_config(config_path):
    with open(config_path, 'rb') as f:
        data = tomllib.load(f)

    return data

def main() -> None:
    args = parser.parse_args()

    os.makedirs('/'.join(args.config.split('/')[:-1]), exist_ok=True)

    if not os.path.exists(args.config):
        open(args.config, 'w').close()

    config = parse_config(args.config)

    if '__config__' not in config:
        print('Missing __config__ section in config file.')
        sys.exit(1)
    
    for key in ['oldver', 'newver', 'install_cmd']:
        if key not in config['__config__']:
            print(f'Missing {key} in __config__ section of the config file.')
            sys.exit(1)

    subprocess.call(['nvchecker', '-c', args.config, '-l', 'error'])

    output = json.loads(subprocess.check_output(['nvcmp', '-c', args.config, '-j']).strip())

    subprocess.call(['nvcmp', '-c', args.config])

    if len(output) == 0:
        print('Nothing to do.')
        sys.exit()

    answer = input('Should the following update(s) be applied ? (Y/N) ')

    if answer.lower() != 'y':
        sys.exit()

    tmpdir = tempfile.gettempdir()

    for update in output:
        package = update['name']
        version = update['newver']

        params = config[package]

        url = params['rpmdurl']
        prev_char = url[0]
        scanning = False
        matches = []
        current = ''

        for c in url[1:]:
            if scanning:
                current += c
            
            if prev_char == '$' and c == '{':
                scanning = True
                current = ''

            if c == '}':
                matches.append(current[:-1])
                scanning = False

            prev_char = c

        for match in matches:
            url = url.replace('${' + match + '}', eval(match))

        print()
        print(f'Downloading {package}...\n')

        filename = url.split('/')[-1]

        file = wget.download(url, tmpdir + f'/{filename}')

        print()
        print(f'Installing {package}...\n')

        code = subprocess.call(config['__config__']['install_cmd'].split(' ') + [file])

        if code != 0:
            sys.exit(code)

        print()
        print('Done.')


    subprocess.call(['nvtake', '-c', args.config, '--all'])

if __name__ == '__main__':
    main()