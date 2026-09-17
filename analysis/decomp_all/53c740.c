
int FUN__text__0053c740(int param_1,int *param_2,int *param_3)

{
  int *piVar1;
  uint uVar2;
  int *piVar3;
  int *piVar4;
  int iVar5;
  int *piVar6;
  int local_24 [2];
  uint local_1c;
  uint local_c;
  int local_8;
  
  if (param_2 == (int *)0x0) {
    iVar5 = -0x7789f794;
  }
  else if ((((*(int *)(param_1 + 0x30) == 0) &&
            ((**(code **)(*param_2 + 0x20))(param_2,local_24),
            local_24[0] == *(int *)(param_1 + 0x14))) &&
           (uVar2 = *(uint *)(param_1 + 0xc), local_c == uVar2)) &&
          (local_8 == *(int *)(param_1 + 0x10))) {
    *(uint *)(param_1 + 0x34) = local_1c & 1;
    if (param_3 == (int *)0x0) {
      *(undefined4 *)(param_1 + 0x3c) = 0;
      *(undefined4 *)(param_1 + 0x4c) = 0;
      *(undefined4 *)(param_1 + 0x40) = 0;
      *(uint *)(param_1 + 0x44) = uVar2;
      *(undefined4 *)(param_1 + 0x50) = 0x3f800000;
      *(int *)(param_1 + 0x48) = *(int *)(param_1 + 0x10);
    }
    else {
      piVar6 = (int *)(param_1 + 0x3c);
      for (iVar5 = 6; iVar5 != 0; iVar5 = iVar5 + -1) {
        *piVar6 = *param_3;
        param_3 = param_3 + 1;
        piVar6 = piVar6 + 1;
      }
      if ((uVar2 < (uint)(*(int *)(param_1 + 0x44) + *(int *)(param_1 + 0x3c))) ||
         (*(uint *)(param_1 + 0x10) < (uint)(*(int *)(param_1 + 0x48) + *(int *)(param_1 + 0x40))))
      {
        return -0x7789f794;
      }
    }
    if ((((*(int *)(param_1 + 0x20) != 0) || ((local_1c & 1) != 0)) ||
        (iVar5 = (**(code **)(**(int **)(param_1 + 8) + 100))
                           (*(int **)(param_1 + 8),uVar2,*(undefined4 *)(param_1 + 0x10),
                            *(undefined4 *)(param_1 + 0x14),0,1,(int *)(param_1 + 0x20)), -1 < iVar5
        )) && (((*(int *)(param_1 + 0x28) != 0 || (*(int *)(param_1 + 0x18) == 0)) ||
               (iVar5 = (**(code **)(**(int **)(param_1 + 8) + 0x68))
                                  (*(int **)(param_1 + 8),*(undefined4 *)(param_1 + 0xc),
                                   *(undefined4 *)(param_1 + 0x10),*(undefined4 *)(param_1 + 0x1c),0
                                   ,(int *)(param_1 + 0x28)), -1 < iVar5)))) {
      piVar6 = (int *)(param_1 + 0x38);
      if (*piVar6 == 0) {
        (**(code **)(**(int **)(param_1 + 8) + 0xd0))(*(int **)(param_1 + 8));
        (**(code **)(**(int **)(param_1 + 8) + 0xa0))(*(int **)(param_1 + 8),param_1 + 0x3c);
        (**(code **)(**(int **)(param_1 + 8) + 0xd4))(*(int **)(param_1 + 8),piVar6);
      }
      piVar1 = (int *)(param_1 + 0x24);
      piVar3 = (int *)*piVar1;
      if (piVar3 != (int *)0x0) {
        (**(code **)(*piVar3 + 8))(piVar3);
        *piVar1 = 0;
      }
      piVar3 = (int *)(param_1 + 0x2c);
      piVar4 = (int *)*piVar3;
      if (piVar4 != (int *)0x0) {
        (**(code **)(*piVar4 + 8))(piVar4);
        *piVar3 = 0;
      }
      (**(code **)(**(int **)(param_1 + 8) + 0xdc))(*(int **)(param_1 + 8),*piVar6);
      (**(code **)(**(int **)(param_1 + 8) + 0x80))(*(int **)(param_1 + 8),piVar1);
      (**(code **)(**(int **)(param_1 + 8) + 0x84))(*(int **)(param_1 + 8),piVar3);
      piVar4 = param_2;
      if (*(int *)(param_1 + 0x34) == 0) {
        piVar4 = *(int **)(param_1 + 0x20);
      }
      iVar5 = (**(code **)(**(int **)(param_1 + 8) + 0x7c))
                        (*(int **)(param_1 + 8),piVar4,*(undefined4 *)(param_1 + 0x28));
      if (-1 < iVar5) {
        iVar5 = (**(code **)(**(int **)(param_1 + 8) + 0xa0))(*(int **)(param_1 + 8),param_1 + 0x3c)
        ;
        if (iVar5 < 0) {
          (**(code **)(**(int **)(param_1 + 8) + 0x7c))(*(int **)(param_1 + 8),*piVar1,*piVar3);
          param_1 = iVar5;
        }
        else {
          iVar5 = (**(code **)(**(int **)(param_1 + 8) + 0x88))(*(int **)(param_1 + 8));
          if (-1 < iVar5) {
            *(int **)(param_1 + 0x30) = param_2;
            (**(code **)(*param_2 + 4))(param_2);
            return 0;
          }
          (**(code **)(**(int **)(param_1 + 8) + 0x7c))(*(int **)(param_1 + 8),*piVar1,*piVar3);
          (**(code **)(**(int **)(param_1 + 8) + 0xd8))(*(int **)(param_1 + 8),*piVar6);
          param_1 = iVar5;
        }
        piVar6 = (int *)*piVar1;
        if (piVar6 != (int *)0x0) {
          (**(code **)(*piVar6 + 8))(piVar6);
          *piVar1 = 0;
        }
        piVar6 = (int *)*piVar3;
        iVar5 = param_1;
        if (piVar6 != (int *)0x0) {
          (**(code **)(*piVar6 + 8))(piVar6);
          *piVar3 = 0;
        }
      }
    }
  }
  else {
    iVar5 = -0x7fffbffb;
  }
  return iVar5;
}

