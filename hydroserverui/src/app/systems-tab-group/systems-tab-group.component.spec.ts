import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SystemsTabGroupComponent } from './systems-tab-group.component';

describe('SystemsTabGroupComponent', () => {
  let component: SystemsTabGroupComponent;
  let fixture: ComponentFixture<SystemsTabGroupComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ SystemsTabGroupComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(SystemsTabGroupComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
