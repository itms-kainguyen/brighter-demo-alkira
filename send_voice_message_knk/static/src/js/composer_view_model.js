/** @odoo-module **/

import { registerPatch } from '@mail/model/model_core';
import { attr } from '@mail/model/model_field';
var rpc = require('web.rpc');

const recorder = new MicRecorder({
    bitRate: 128
  });
  

 // send_sms_view_form


registerPatch({
    name: 'ComposerView',
    recordMethods: {
        send_sms(event) {


    
    

        },
        onStartRecording(event) {
            const isMobile = {
              // Code to check the user's OS and prevent default functions
              Android: function() {
                return navigator.userAgent.match(/Android/i);
              },
              BlackBerry: function() {
                return navigator.userAgent.match(/BlackBerry/i);
              },
              iOS: function() {
                return navigator.userAgent.match(/iPhone|iPad|iPod/i);
              },
              Opera: function() {
                return navigator.userAgent.match(/Opera Mini/i);
              },
              Windows: function() {
                return navigator.userAgent.match(/IEMobile/i) || navigator.userAgent.match(/WPDesktop/i);
              },
              any: function() {
                return (isMobile.Android() || isMobile.BlackBerry() || isMobile.iOS() || isMobile.Opera() || isMobile.Windows());
              }
            };
          
            if (isMobile.any()) {
              event.preventDefault();
            }
          
            $(".o_Composer_buttonRecording").addClass("recording");
            var self = this;
            if (!(navigator.mediaDevices && navigator.mediaDevices.getUserMedia)) {
                return Promise.reject(new Error('mediaDevices API or getUserMedia method is not supported in this browser.'));
            }

            else {
                navigator.mediaDevices.getUserMedia({ audio: true })
                recorder.start().then(() => {
                    console.log('Recording started');
                  }).catch((error) => {
                    // Failed to start recording
                    console.error('Failed to start recording:', error);
                  });
            }
          },
          
         async onStopRecording() {

            $(".o_Composer_buttonRecording").removeClass("recording");
            var self = this;
            const [buffer, blob] = await recorder.stop().getMp3();
            console.log(buffer, blob); 

            // fetch the audio file data in binary format

            const response = await fetch(URL.createObjectURL(blob));
            const player = new Audio(URL.createObjectURL(blob));
            player.controls = true;
            self.loadURLToInputFiled(player.src);

          },
        loadURLToInputFiled(url){
          var self = this;
          this.getImgURL(url, (imgBlob)=>{
            let fileName = moment(new Date()).format('MM-DD-YYYY hh:mm:ss')+'.mp3';
            let file = new File([imgBlob], fileName,{type:"audio/mp3", lastModified:new Date().getTime()}, 'utf-8');
            let container = new DataTransfer(); 
            container.items.add(file);
            self.fileUploader.fileInput.files = container.files;
            self.fileUploader.uploadFiles(self.fileUploader.fileInput.files);
          })
          window.URL.revokeObjectURL(url)
        },
        getImgURL(url, callback){
          var xhr = new XMLHttpRequest();
          xhr.onload = function() {
              callback(xhr.response);
          };
          xhr.open('GET', url);
          xhr.responseType = 'blob';
          xhr.send();
        }
    }
});

registerPatch({
    name: 'Attachment',
    fields: {
        attachUrl: attr({
            compute() {
                if (!this.accessToken && this.originThread && this.originThread.model === 'mail.channel') {
                    return `/mail/channel/${this.originThread.id}/attachment/${this.id}`;
                }
                const accessToken = this.accessToken ? `access_token=${this.accessToken}&` : '';
                return `/web/content/ir.attachment/${this.id}/datas`;
            },
        }),
    }
});
