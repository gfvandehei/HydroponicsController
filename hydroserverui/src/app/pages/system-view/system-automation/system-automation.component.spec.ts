import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SystemAutomationComponent } from './system-automation.component';

describe('SystemAutomationComponent', () => {
  let component: SystemAutomationComponent;
  let fixture: ComponentFixture<SystemAutomationComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ SystemAutomationComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(SystemAutomationComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
