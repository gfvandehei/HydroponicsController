import { ComponentFixture, TestBed } from '@angular/core/testing';

import { DualCircleGraphComponent } from './dual-circle-graph.component';

describe('DualCircleGraphComponent', () => {
  let component: DualCircleGraphComponent;
  let fixture: ComponentFixture<DualCircleGraphComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ DualCircleGraphComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(DualCircleGraphComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
