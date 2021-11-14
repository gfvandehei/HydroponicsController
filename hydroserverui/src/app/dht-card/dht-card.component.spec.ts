import { ComponentFixture, TestBed } from '@angular/core/testing';

import { DhtCardComponent } from './dht-card.component';

describe('DhtCardComponent', () => {
  let component: DhtCardComponent;
  let fixture: ComponentFixture<DhtCardComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ DhtCardComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(DhtCardComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
