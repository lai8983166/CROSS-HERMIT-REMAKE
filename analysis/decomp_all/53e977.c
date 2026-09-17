
int FUN__text__0053e977(int *param_1)

{
  int *piVar1;
  int *piVar2;
  int iVar3;
  int *piVar4;
  int local_8;
  
  piVar2 = param_1;
  iVar3 = FUN__text__0053e8a3();
  if (-1 < iVar3) {
    (**(code **)(*(int *)piVar2[2] + 0x7c))((int *)piVar2[2],piVar2[10],piVar2[0xb]);
    (**(code **)(*(int *)piVar2[2] + 0xd8))((int *)piVar2[2],piVar2[0x11c]);
    piVar4 = (int *)piVar2[10];
    if (piVar4 != (int *)0x0) {
      (**(code **)(*piVar4 + 8))(piVar4);
      piVar2[10] = 0;
    }
    piVar4 = (int *)piVar2[0xb];
    if (piVar4 != (int *)0x0) {
      (**(code **)(*piVar4 + 8))(piVar4);
      piVar2[0xb] = 0;
    }
    if (piVar2[0x118] == 1) {
      piVar4 = (int *)piVar2[0xd];
      if (piVar4 != (int *)0x0) {
        (**(code **)(*piVar4 + 8))(piVar4);
        piVar2[0xd] = 0;
      }
    }
    else {
      piVar4 = piVar2 + 0xe;
      local_8 = 2;
      do {
        piVar1 = (int *)*piVar4;
        if (piVar1 != (int *)0x0) {
          if ((piVar4[4] == 0) && (piVar4[2] != 0)) {
            (**(code **)(*piVar1 + 0x3c))(piVar1,0,&param_1);
            (**(code **)(*(int *)piVar2[2] + 0x70))((int *)piVar2[2],piVar4[2],0,0,param_1,0);
            if (param_1 != (int *)0x0) {
              (**(code **)(*param_1 + 8))(param_1);
              param_1 = (int *)0x0;
            }
          }
          piVar1 = (int *)*piVar4;
          if (piVar1 != (int *)0x0) {
            (**(code **)(*piVar1 + 8))(piVar1);
            *piVar4 = 0;
          }
        }
        piVar4 = piVar4 + 1;
        local_8 = local_8 + -1;
      } while (local_8 != 0);
    }
    piVar2[0x118] = 0;
    iVar3 = 0;
  }
  return iVar3;
}

