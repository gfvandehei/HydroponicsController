import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SystemsHomeComponent } from './systems-home.component';

describe('SystemsHomeComponent', () => {
  let component: SystemsHomeComponent;
  let fixture: ComponentFixture<SystemsHomeComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ SystemsHomeComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(SystemsHomeComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
