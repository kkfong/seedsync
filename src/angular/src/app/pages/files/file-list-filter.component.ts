import {ChangeDetectionStrategy, Component} from '@angular/core';
import {Observable} from "rxjs/Observable";

import {LoggerService} from "../../common/logger.service"
import {ViewFileFilterService} from "../../view/view-file-filter.service";
import {ViewFileFilter} from "../../view/view-file-filter";
import {ViewFile} from "../../view/view-file";

@Component({
    selector: 'file-list-filter',
    providers: [],
    templateUrl: './file-list-filter.component.html',
    styleUrls: ['./file-list-filter.component.scss'],
    changeDetection: ChangeDetectionStrategy.OnPush
})

export class FileListFilterComponent {
    public filter: Observable<ViewFileFilter>;

    public filterName: string = "";

    constructor(private _logger: LoggerService,
                private viewFileFilterService: ViewFileFilterService) {
        this.filter = this.viewFileFilterService.filter;
    }

    onFilterAll() {
        this.viewFileFilterService.filterStatus(null);
    }

    onFilterDownloaded() {
        this.viewFileFilterService.filterStatus(ViewFile.Status.DOWNLOADED);
    }

    onFilterDownloading() {
        this.viewFileFilterService.filterStatus(ViewFile.Status.DOWNLOADING);
    }

    onFilterQueued() {
        this.viewFileFilterService.filterStatus(ViewFile.Status.QUEUED);
    }

    onFilterStopped() {
        this.viewFileFilterService.filterStatus(ViewFile.Status.STOPPED);
    }

    onFilterDefault() {
        this.viewFileFilterService.filterStatus(ViewFile.Status.DEFAULT);
    }

    onFilterByName(name: string) {
        this.filterName = name;
        this.viewFileFilterService.filterName(this.filterName);
    }
}
