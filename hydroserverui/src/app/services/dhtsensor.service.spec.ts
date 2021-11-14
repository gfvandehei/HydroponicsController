import { TestBed } from '@angular/core/testing';

import { DhtsensorService } from './dhtsensor.service';

describe('DhtsensorService', () => {
  let service: DhtsensorService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(DhtsensorService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
