import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PumpInfoCardComponent } from './pump-info-card.component';

describe('PumpInfoCardComponent', () => {
  let component: PumpInfoCardComponent;
  let fixture: ComponentFixture<PumpInfoCardComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ PumpInfoCardComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(PumpInfoCardComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
