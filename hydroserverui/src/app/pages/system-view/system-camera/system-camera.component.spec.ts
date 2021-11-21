import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SystemCameraComponent } from './system-camera.component';

describe('SystemCameraComponent', () => {
  let component: SystemCameraComponent;
  let fixture: ComponentFixture<SystemCameraComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ SystemCameraComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(SystemCameraComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
