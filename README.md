# dds-extractor

Import or export DDS textures for Senran Kagura: Peach Beach Splash

> [!WARNING]
> The tool is still in development and is not fully stable!

## About the script

A simple extractor/importer script catered to searching whatever .cat file you throw at it.
The script can handle simple DDS textures as well as more complex ones, including:
* cube maps
* mipmaps

The support for these two should let you easily work with most types of textures in PBS with little effort.

## Important

1. Unlike other DDS tools that are out there, **this tool does not respect the original file names of the DDS images inside .cat files**. Instead it applies a different name to each extracted file in the following format:

	catfile_index.dds

Where catfile is the .cat on which the script operates, and index is where the DDS match was found with respect to other entries. First DDS find will have index 1, second will have index 2, and so on. This might change in the future, but at the moment that's just how it is.

2. One important distinction of this tool is that the **first argument is treated as a wildcard**, not as a whole word. This basically means that if you run the following command:

```
ddsx.py gun ...
```
The script will search for every .cat file containing the word "gun". This is powerful for extracting/importing using multiple files simultaneously. However, you have to use careful not to accidentally modify files you didn't want.

4. Make sure, when you import textures, **file size and compression format match the original texture**. If the file size is off then the game will simply crash.

Right now the script doesn't tell you the compression used by a particular texture. This will be implemented later. For now, you can view the compression at the top of the .dds file using a hex editor. These images typically use either DXT1 or DXT5 compression.

The script will search for every .cat file containing the word "gun". This is powerful for when you want to extract/import into multiple files simultaneously. However, you do have to use careful not to accidentally modify files you didn't want.

## Setup

1. Make sure you have Python 3.13 or higher installed on your system
2. Download the project
3. Navigate to the project using the [command line](https://www.geeksforgeeks.org/techtips/change-directories-in-command-prompt/)

## How to use

Simply run ddsx.py from the command line and pass options to the script as follows:

```
ddsx.py wildcard [options] [arguments]
```

wildcard 	- Search for files whose names contain a particular word.

options		- Tell the script what to do. The following options are currently available:
*	-l									:	List DDS entries inside the cat file
*	-e [index] [path_to_folder]			:	Export a DDS texture from the container based on an index. Texture is exported to the specified path
*	-E [path_to_folder]					:	Export all DDS textures the script can find to the specified path
*	-i [index] [path_to_file]			:	Insert a DDS texture based on the index
*	-I [path_to_folder] [shared_name]	:	Insert multiple textures at once into a .cat file whose names begin with shared name argument

arguments	- Different values provided to options

## Usage

For simplicity, the paths provided in the examples are relative. Do note that absolute paths work as well.

Examples demonstrating the script:

1. List all textures present in gun_mis_F.cat (level 10 spray gun model container):

```
ddsx.py gun_mis_F.cat -l
```

This will display the indexes available to us that we can work with.

2. Extract parts and base texture of the spray gun to a folder named "stuff":

```
ddsx.py gun_mis_F.cat -e 1 stuff\
ddsx.py gun_mis_F.cat -e 3 stuff\
```

The textures extracted after these commands will be called gun_mis_F_1.dds and gun_mis_F_3.dds, respectively. It is recommended to keep this same naming convention for when you decide to re-import these textures.

3. You modified the spray gun parts texture (using GIMP or what have you) and now want to import it to see the changes in-game. Try the following:

```
ddsx.py gun_mis_F.cat -i 1 .
```

Dot means "current directory" relative to where the script lives. In other words, if your script is located in C:\Games\ddsx.py, then . would be the same as saying C:\Games. The script would then search this directory for the texture to import.

4. Excited about what textures comprise the Tropical Athletics map in PBS, you decided to export them all! Simply do the following:

```
ddsx.py bg00.cat -E map_stuff\
```

5. Getting curious about character panels, you decided to export all textures from all player .cat files (pl01.cat, pl02.cat, ..., pl50.cat) using the following command:

```
ddsx.py pl -E panels\
```

Which treats pl as a wildcard to detect all files containing the "pl" word, then extracting all textures inside of them into the panels folder

6. While extracting plxx.cat files, you had a funny idea: "what if I write the same image across *all* of these different containers using my mydog_01.dds file? Instead of looking at Asuka, Ikagura and so on, I'll just replace them all with a picture of my dog. I'm incredibly smart!"

If that is you then you are in luck! Even with such an esoteric request, the script can fulfill it like so:

```
ddsx.py pl -I panels\ mydog
```

This may be a bit hard to understand so let's break it down:
*	First argument "pl" selects all the .cat files containing the "pl" word, but this time for importing rather than exporting
*	"panels" is where our custom image, mydog_1.cat, exists. If it lives in the same place as the script, use the dot (.), otherwise specify a different folder where your image lives
*	"mydog" is the name shared by multiple for mass importing to .cat files. This helps with automation and consistency.
    * The script expects that a file whose name starts with this argument is also followed by _n.dds, where n is the index to which the image maps
    * If your file is called something else, like pl01_1.dds, then this arguments should be "pl01". The name must be specific, so "pl" won't work here

Assuming panels contains only mydog_1.dds, this file will be written to *aLL* plxx.cat files at index 1.

If the panels folder contained multiple mydog files, for example mydog_2.dds and mydog_3.dds, multiple files would be written per .cat file instead of just one.

Mass importing is still in its raw state, but can be useful for more complex modding scenarios once you understand it.

## Credits

Written by FX