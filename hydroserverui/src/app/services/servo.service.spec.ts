import { TestBed } from '@angular/core/testing';

import { ServoService } from './servo.service';

describe('ServoService', () => {
  let service: ServoService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(ServoService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
