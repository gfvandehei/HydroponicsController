import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PumpScheduleDisplayComponent } from './pump-schedule-display.component';

describe('PumpScheduleDisplayComponent', () => {
  let component: PumpScheduleDisplayComponent;
  let fixture: ComponentFixture<PumpScheduleDisplayComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ PumpScheduleDisplayComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(PumpScheduleDisplayComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
