namespace GBXPos
{
    partial class Form1
    {
        /// <summary>
        /// Required designer variable.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        /// Clean up any resources being used.
        /// </summary>
        /// <param name="disposing">true if managed resources should be disposed; otherwise, false.</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Windows Form Designer generated code

        /// <summary>
        /// Required method for Designer support - do not modify
        /// the contents of this method with the code editor.
        /// </summary>
        private void InitializeComponent()
        {
            this.components = new System.ComponentModel.Container();
            System.ComponentModel.ComponentResourceManager resources = new System.ComponentModel.ComponentResourceManager(typeof(Form1));
            this.openFileDialogReplayGbx = new System.Windows.Forms.OpenFileDialog();
            this.btnSelectFile = new System.Windows.Forms.Button();
            this.label1 = new System.Windows.Forms.Label();
            this.flexSelection = new System.Windows.Forms.FlowLayoutPanel();
            this.label3 = new System.Windows.Forms.Label();
            this.flexTrackInfo = new System.Windows.Forms.FlowLayoutPanel();
            this.titleTrackInfo = new System.Windows.Forms.Label();
            this.flowLayoutPanel2 = new System.Windows.Forms.FlowLayoutPanel();
            this.label2 = new System.Windows.Forms.Label();
            this.replayInfoText = new System.Windows.Forms.Label();
            this.flexActions = new System.Windows.Forms.FlowLayoutPanel();
            this.label4 = new System.Windows.Forms.Label();
            this.btnCreateInfoFile = new System.Windows.Forms.Button();
            this.cameraKeyframesText = new System.Windows.Forms.Label();
            this.flowLayoutPanel4 = new System.Windows.Forms.FlowLayoutPanel();
            this.notifyIcon1 = new System.Windows.Forms.NotifyIcon(this.components);
            this.flexSelection.SuspendLayout();
            this.flexTrackInfo.SuspendLayout();
            this.flowLayoutPanel2.SuspendLayout();
            this.flexActions.SuspendLayout();
            this.flowLayoutPanel4.SuspendLayout();
            this.SuspendLayout();
            // 
            // openFileDialogReplayGbx
            // 
            resources.ApplyResources(this.openFileDialogReplayGbx, "openFileDialogReplayGbx");
            this.openFileDialogReplayGbx.SupportMultiDottedExtensions = true;
            this.openFileDialogReplayGbx.FileOk += new System.ComponentModel.CancelEventHandler(this.openFileDialog1_FileOk);
            // 
            // btnSelectFile
            // 
            this.btnSelectFile.AllowDrop = true;
            resources.ApplyResources(this.btnSelectFile, "btnSelectFile");
            this.btnSelectFile.Name = "btnSelectFile";
            this.btnSelectFile.UseVisualStyleBackColor = true;
            this.btnSelectFile.Click += new System.EventHandler(this.button1_Click);
            // 
            // label1
            // 
            resources.ApplyResources(this.label1, "label1");
            this.label1.Name = "label1";
            // 
            // flexSelection
            // 
            resources.ApplyResources(this.flexSelection, "flexSelection");
            this.flexSelection.AllowDrop = true;
            this.flexSelection.CausesValidation = false;
            this.flexSelection.Controls.Add(this.label3);
            this.flexSelection.Controls.Add(this.btnSelectFile);
            this.flexSelection.Controls.Add(this.label1);
            this.flexSelection.Name = "flexSelection";
            // 
            // label3
            // 
            resources.ApplyResources(this.label3, "label3");
            this.label3.Name = "label3";
            // 
            // flexTrackInfo
            // 
            resources.ApplyResources(this.flexTrackInfo, "flexTrackInfo");
            this.flexTrackInfo.CausesValidation = false;
            this.flexTrackInfo.Controls.Add(this.titleTrackInfo);
            this.flexTrackInfo.Controls.Add(this.flowLayoutPanel2);
            this.flexTrackInfo.Name = "flexTrackInfo";
            // 
            // titleTrackInfo
            // 
            resources.ApplyResources(this.titleTrackInfo, "titleTrackInfo");
            this.titleTrackInfo.Name = "titleTrackInfo";
            // 
            // flowLayoutPanel2
            // 
            resources.ApplyResources(this.flowLayoutPanel2, "flowLayoutPanel2");
            this.flowLayoutPanel2.Controls.Add(this.label2);
            this.flowLayoutPanel2.Controls.Add(this.replayInfoText);
            this.flowLayoutPanel2.Name = "flowLayoutPanel2";
            // 
            // label2
            // 
            resources.ApplyResources(this.label2, "label2");
            this.label2.Name = "label2";
            // 
            // replayInfoText
            // 
            resources.ApplyResources(this.replayInfoText, "replayInfoText");
            this.replayInfoText.Name = "replayInfoText";
            // 
            // flexActions
            // 
            resources.ApplyResources(this.flexActions, "flexActions");
            this.flexActions.Controls.Add(this.label4);
            this.flexActions.Controls.Add(this.btnCreateInfoFile);
            this.flexActions.Controls.Add(this.cameraKeyframesText);
            this.flexActions.Name = "flexActions";
            // 
            // label4
            // 
            resources.ApplyResources(this.label4, "label4");
            this.label4.Name = "label4";
            // 
            // btnCreateInfoFile
            // 
            resources.ApplyResources(this.btnCreateInfoFile, "btnCreateInfoFile");
            this.btnCreateInfoFile.Name = "btnCreateInfoFile";
            this.btnCreateInfoFile.UseVisualStyleBackColor = true;
            this.btnCreateInfoFile.Click += new System.EventHandler(this.btnCreateInfoFile_Click);
            // 
            // cameraKeyframesText
            // 
            resources.ApplyResources(this.cameraKeyframesText, "cameraKeyframesText");
            this.cameraKeyframesText.FlatStyle = System.Windows.Forms.FlatStyle.System;
            this.cameraKeyframesText.Name = "cameraKeyframesText";
            // 
            // flowLayoutPanel4
            // 
            this.flowLayoutPanel4.AllowDrop = true;
            resources.ApplyResources(this.flowLayoutPanel4, "flowLayoutPanel4");
            this.flowLayoutPanel4.Controls.Add(this.flexSelection);
            this.flowLayoutPanel4.Controls.Add(this.flexTrackInfo);
            this.flowLayoutPanel4.Controls.Add(this.flexActions);
            this.flowLayoutPanel4.Name = "flowLayoutPanel4";
            // 
            // notifyIcon1
            // 
            resources.ApplyResources(this.notifyIcon1, "notifyIcon1");
            // 
            // Form1
            // 
            this.AllowDrop = true;
            resources.ApplyResources(this, "$this");
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.Controls.Add(this.flowLayoutPanel4);
            this.MaximizeBox = false;
            this.Name = "Form1";
            this.Load += new System.EventHandler(this.Form1_Load);
            this.flexSelection.ResumeLayout(false);
            this.flexSelection.PerformLayout();
            this.flexTrackInfo.ResumeLayout(false);
            this.flexTrackInfo.PerformLayout();
            this.flowLayoutPanel2.ResumeLayout(false);
            this.flowLayoutPanel2.PerformLayout();
            this.flexActions.ResumeLayout(false);
            this.flexActions.PerformLayout();
            this.flowLayoutPanel4.ResumeLayout(false);
            this.flowLayoutPanel4.PerformLayout();
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion

        private System.Windows.Forms.OpenFileDialog openFileDialogReplayGbx;
        private System.Windows.Forms.Button btnSelectFile;
        private System.Windows.Forms.Label label1;
        private System.Windows.Forms.FlowLayoutPanel flexSelection;
        private System.Windows.Forms.FlowLayoutPanel flexTrackInfo;
        private System.Windows.Forms.Label titleTrackInfo;
        private System.Windows.Forms.Label replayInfoText;
        private System.Windows.Forms.FlowLayoutPanel flowLayoutPanel2;
        private System.Windows.Forms.Label label2;
        private System.Windows.Forms.Label label3;
        private System.Windows.Forms.FlowLayoutPanel flexActions;
        private System.Windows.Forms.Button btnCreateInfoFile;
        private System.Windows.Forms.Label label4;
        private System.Windows.Forms.FlowLayoutPanel flowLayoutPanel4;
        private System.Windows.Forms.Label cameraKeyframesText;
        private System.Windows.Forms.NotifyIcon notifyIcon1;
    }
}

