import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PumpCardComponent } from './pump-card.component';

describe('PumpCardComponent', () => {
  let component: PumpCardComponent;
  let fixture: ComponentFixture<PumpCardComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ PumpCardComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(PumpCardComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
