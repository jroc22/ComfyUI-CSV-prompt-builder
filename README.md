
# ComfyUI-CSV-prompt-builder

This is a simple node for creating prompts using a .csv file. I created this node as an easy way to output different prompts each time a workflow is run. It serves my needs well so I figured I would share in case someone else could benefit from it.

Please keep in mind I am not a programmer and this is my first node attempt (and first coding project). There may be some poorly written code or functionality that can be improved. If you have any recommendations for changes or improvements to the code let me know, I'm eager to learn and theres some things I just couldn't figure out or get to work.

## Installation

Just clone the repo as you would any other node, or download the zip and place the "ComfyUI-CSV-prompt-builder" folder in your custom_nodes directory.

```bash
# To clone the repo, navigate to the ComfyUI custom_nodes directory and open a command prompt
# Clone the repository
git clone https://github.com/yourusername/your-repository.git

```

## Usage

To get started, simply add the node to your workflow. The node outputs text, so you will need to encode the text for generation. Also provided is an example workflow with the node added along with pythongosssss' "Show Text" node from https://github.com/pythongosssss/ComfyUI-Custom-Scripts (highly recommend if you don't already have it).

The node reads the contents of the selected .csv file and displays the following fields for each column:

    • {column A header}_mode: This is how the value will be selected for output. The options are:
        
        • Fixed: Output the value chosen in the following "_val" field.
        • Randomize: Output a random value from the column (regardless of selected "_val").
        • Cycle: Output the values in the column in order from top to bottom. When it reaches the end of the column, it will start from the beginning again.

    • {column A header}_val: The value to output when using Fixed mode.

    • {column A header}_weight: How to weight the output value. Will add partenthesis and the weight factor (e.g., (a cat:1.25))

    • {column A}_to_{column B}: The separator between this column and the next column (default is ", "). This is a sinlge-line string field. While it's intended for the separator, you can turn any of them into an input and connect a multi-line string node to more easily add any amount of text between two columns. Just be sure to begin and end with the desired separator(s) and spaces -- e.g. ", {your text}, "

### Some Important Notes About Node Usage and CSV Files

All CSV files must go in the "promt_sets" folder, and esnure there is at least one CSV file in there at all times. There is no hard limit set on the number of CSV files you can have in there, but I imagine after ~100 performance would be impacted.

All CSV files you add to the folder must include column headers on the first row -- the column headers are used to name the fields on the node. All the values in the subsequent rows of that column will be used as output. It's a basic set up, but you can look at either of the provided example CSV files for a simple outline.

There is no hard limit set on the number of columns or rows your CSV file can have. I've only really tested up to 30 columns with 50-100 rows each. A significant number of columns and rows may lead to performance issues, so be warned. At 30 columns I had no problems other than the Node was quite tall visually.

#### Multiple Node Instances

Due to how the CSV file switching is set up, this node does not currently support multiple instances with DIFFERENT CSV file sources. You may have multiple instances that use the same CSV file. If you want to use multiple instances of the Node, I recommend turning the "csv_file" field into an input on each instance, and connecting the same Combo node to each. This way, when you change the CSV file it will correctly update for each instance (if you don't do this, after the restart you will need to swtich the CSV file drop-down to the correct CSV file on each other instance of the node, or it will fail).

If anyone knows how to allow multiple instances with difference CSV sources and wants to share, please do!

#### CSV File Handling

The CSV handling isn't great tbh. I added the ability to swtich between different CSV files rather than just having a single CSV file that had to be updated/replaced, and it mostly works fine, but it did introduce a some potential issues. Anyway, here's a quick rundown of how it works and what to be aware of:

##### Changing the CSV File

After changing the CSV file in the Node drop-down field, you will need to run the node once and then Restart ComfyUI to see the changes. You should get a notification after changing the CSV file and running it once, telling you to restart ComfyUI. This is the only way I could make it possible to switch CSV files directly on the node. It's not amazing, but it works.

    • One note about CSV switching: if you change the drop-down (select a new CSV), run the node, and then change the drop-down AGAIN to a new CSV file BEFORE restarting ComfyUI, the node will load with the first selected CSV file config, but the drop-down will show the second CSV filename in it (I think this is due to how ComfyUI caches workflows, but I don't really know). Then, when you try to run it, it will again tell you to restart because now it is trying to load that second CSV file. So the moral of the story is don't do that.

Using the correct method of switching CSV files should give you no trouble -- again, the process is: 

    • Select a new CSV File in the drop-down menu.
    • Run the node once (and see notification to restart ComfyUI).
    • Restart ComfyUI.

##### Updating the Loaded CSV File

Due to how the CSV files are cached, if you make an update to and replace the CSV file you're currently using in the Node without changing the filename (e.g., just by adding values to a column or changing a header), you will need to Restart ComfyUI to see the changes -- the node will not reflect the changes after Refreshing.

##### Deleting the Loaded CSV File

If you DELETE the CSV file that is currently being used by the Node, Restarting ComfyUI should initialize the Node with the first CSV file (by alphabetical sort) in the "prompt_sets" folder. If no CSV files are in the folder, the Node will fail to initialize. 
    • Keep in mind that if you delete a CSV file in this way and Restart ComfyUI, the drop-down may still show the previous CSV filename (the deleted one). If that's the case, make sure to switch it to the correct CSV filename or it will fail to run.

#### CSV Troubleshooting

If for whatever reason the Node keeps failing to initialize, make sure there is at least one CSV file in the "prompt_sets" folder, and then within that folder double check that the "_csv_config.json" file is referencing that CSV file. If the config file is not there, restart ComfyUI and it should be automatically created and default to the first CSV file (by alphabetical sort) in the "prompt_sets" folder. When the Node is run, it updates (or creates) the config file with the selected CSV file. When ComfyUI starts up, it reads the config file to determine how to initialize. As I mentioned I am not a programmer and this CSV file switching was a pain to figure out, so if you encounter issues please share!

## License

This project is licensed under the MIT License.
