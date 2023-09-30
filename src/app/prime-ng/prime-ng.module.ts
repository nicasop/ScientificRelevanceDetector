import { NgModule } from '@angular/core';
import {MenubarModule} from 'primeng/menubar';
import {ButtonModule} from 'primeng/button';
import {PanelModule} from 'primeng/panel';
import {MessagesModule} from 'primeng/messages';
import {MessageModule} from 'primeng/message';
import {FileUploadModule} from 'primeng/fileupload';
import {HttpClientModule} from '@angular/common/http';
import {InputTextModule} from 'primeng/inputtext';
import {ProgressSpinnerModule} from 'primeng/progressspinner';
import {CardModule} from 'primeng/card';
import {ToastModule} from 'primeng/toast';
import {RippleModule} from 'primeng/ripple';
import {TableModule} from 'primeng/table';
import { MultiSelectModule } from 'primeng/multiselect';

@NgModule({
  exports : [
    MenubarModule,
    ButtonModule,
    PanelModule,
    MessagesModule,
    MessageModule,
    FileUploadModule,
    HttpClientModule,
    InputTextModule,
    ProgressSpinnerModule,
    CardModule,
    ToastModule,
    RippleModule,
    TableModule,
    MultiSelectModule

  ]
})
export class PrimeNgModule { }
