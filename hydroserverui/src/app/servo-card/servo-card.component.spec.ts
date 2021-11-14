import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ServoCardComponent } from './servo-card.component';

describe('ServoCardComponent', () => {
  let component: ServoCardComponent;
  let fixture: ComponentFixture<ServoCardComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ ServoCardComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(ServoCardComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
