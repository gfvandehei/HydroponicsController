import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SystemSensorsComponent } from './system-sensors.component';

describe('SystemSensorsComponent', () => {
  let component: SystemSensorsComponent;
  let fixture: ComponentFixture<SystemSensorsComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ SystemSensorsComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(SystemSensorsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
