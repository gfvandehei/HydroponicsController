import { TestBed } from '@angular/core/testing';

import { LoginPromptServiceService } from './login-prompt-service.service';

describe('LoginPromptServiceService', () => {
  let service: LoginPromptServiceService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(LoginPromptServiceService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
