import {Component} from '@angular/core';
import {Observable} from "rxjs/Observable";

import * as Immutable from 'immutable';

import {LoggerService} from "./common/logger.service"
import {ServerStatusService} from "./other/server-status.service";
import {ServerStatus} from "./other/server-status";
import {Notification} from "./other/notification";
import {NotificationService} from "./other/notification.service";

@Component({
    selector: 'header',
    templateUrl: './header.component.html',
    styleUrls: ['./header.component.scss'],
})

export class HeaderComponent {
    // expose Notification type to template
    public Notification = Notification;

    public notifications: Observable<Immutable.List<Notification>>;

    private _prevServerNotification: Notification;

    constructor(private _logger: LoggerService,
                private _serverStatusService: ServerStatusService,
                private _notificationService: NotificationService) {
        this.notifications = this._notificationService.notifications;
        this._prevServerNotification = null;
    }

    public dismiss(notif: Notification) {
        this._notificationService.hide(notif)
    }

    ngOnInit() {
        // Set up a subscriber to show server status notifications
        this._serverStatusService.status.subscribe({
            next: status => {
                if(status.server.up) {
                    // Remove any server notifications we may have added
                    if(this._prevServerNotification != null) {
                        this._notificationService.hide(this._prevServerNotification);
                        this._prevServerNotification = null;
                    }
                } else {
                    // Create a notification
                    let notification = new Notification({
                        level: Notification.Level.DANGER,
                        text: status.server.errorMessage
                    });
                    // Show it, if different from the existing one
                    if(
                            this._prevServerNotification == null ||
                            this._prevServerNotification.text != notification.text
                    ) {
                        // Hide existing, if any
                        if(this._prevServerNotification != null) {
                            this._notificationService.hide(this._prevServerNotification);
                        }
                        this._prevServerNotification = notification;
                        this._notificationService.show(this._prevServerNotification);
                        this._logger.debug("New server notification: %O", this._prevServerNotification);
                    }
                }
            }
        });
    }
}
