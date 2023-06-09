using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using System.IO;
using GBX.NET;
using GBX.NET.Engines.Game;
using GBX.NET.Json;
using TmEssentials;
using static GBX.NET.Engines.Game.CGameCtnReplayRecord;
using System.Text.Json;
using System.Text.Json.Serialization;
using System.Numerics;
using System.Drawing.Drawing2D;
using static GBX.NET.Engines.Game.CGameCtnChallenge;

namespace GBXPos
{
    public partial class Form1 : Form
    {
        private string currentReplayFile = null;
        private CGameCtnReplayRecord node = null;

        public string UnPrettyJson(string unPrettyJson)
        {
            var options = new JsonSerializerOptions()
            {
                WriteIndented = false
            };

            var jsonElement = JsonSerializer.Deserialize<JsonElement>(unPrettyJson);

            return JsonSerializer.Serialize(jsonElement, options);
        }

        public Form1()
        {
            InitializeComponent();
        }

        private void Form1_Load(object sender, EventArgs e)
        {

        }

        private void openFileDialog1_FileOk(object sender, CancelEventArgs e)
        {
            OpenFileDialog someOpenFileDialog = sender as OpenFileDialog;

            label1.Text = someOpenFileDialog.FileName;
            currentReplayFile = someOpenFileDialog.FileName;
            flexTrackInfo.Enabled = true;
            flexActions.Enabled = true;

            node = GameBox.ParseNode<CGameCtnReplayRecord>(currentReplayFile.ToString());

            // _ General Info _ \\

            var map = node.Challenge;
            var ghost = node.Ghosts.FirstOrDefault();

            var mapName = map.MapName;
            var mapUid = map.MapUid;
            var mapId = map.Id;
            var author = map.AuthorLogin;
            var authorTime = map.TMObjective_AuthorTime;
            var blockCount = map.NbBlocks;

            var ghostName = ghost.GhostLogin;
            var ghostTime = ghost.RaceTime;
            var ghostRespawns = ghost.Respawns;

            replayInfoText.Text =
                // Map Info
                $"{mapName}\n{author}\n{authorTime}\n{mapUid}\n{mapId}\n{blockCount}\n\n" +
                // Ghost Info
                $"{ghostName}\n{ghostTime}\n{ghostRespawns}\n";

            // ^ General Info ^ \\\
        }

        private void button1_Click(object sender, EventArgs e)
        {
            openFileDialogReplayGbx.ShowDialog();
        }

        private void btnCreateInfoFile_Click(object sender, EventArgs e)
        {
            // _ Check Clip _ \\

            var _clip = node.Clip;

            if (_clip == null)
            {
                Console.WriteLine("No clip found in selected replay.Gbx file!");
                notifyIcon1.Icon = new Icon(Path.GetFullPath("FileError.ico"));
                notifyIcon1.BalloonTipTitle = "The selected replay has no clip!";
                notifyIcon1.BalloonTipText = "Edit the replay file in the TMNF/TMUF replay editor then try again.";
                notifyIcon1.ShowBalloonTip(100);
                return;
            }

            // ^ Check Clip ^ \\

            // _ Serialize to Json _ \\

            var jsonString = UnPrettyJson(node.ToGbx().ToJson());

            // ^ Serialize to Json ^ \\

            // _ Save Json File _ \\

            var writePath = new DirectoryInfo(Path.GetDirectoryName(Application.ExecutablePath)).Parent.Parent.Parent.Parent;
            string FolderName = writePath.Name;
            string PathStr = writePath.FullName;
            Console.WriteLine(writePath);

            // If the file name is not an empty string open it for saving.
            if (FolderName == "GBXPosBlenderAddon")
            {
                Console.WriteLine("Saved GBXPos JSON file to " + PathStr);
                File.WriteAllText(PathStr + "\\NewReplay.json", jsonString);
            }

            Close();

            // ^ Save Json File ^ \\
        }
    }
}
