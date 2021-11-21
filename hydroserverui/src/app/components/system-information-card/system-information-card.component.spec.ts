import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SystemInformationCardComponent } from './system-information-card.component';

describe('SystemInformationCardComponent', () => {
  let component: SystemInformationCardComponent;
  let fixture: ComponentFixture<SystemInformationCardComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ SystemInformationCardComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(SystemInformationCardComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
