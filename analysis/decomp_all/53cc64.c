
int __thiscall FUN__text__0053cc64(int param_1,undefined4 param_2)

{
  int *piVar1;
  int iVar2;
  undefined1 local_28 [8];
  uint local_20;
  int *local_8;
  
  local_8 = (int *)0x0;
  if (*(int *)(param_1 + 0x460) == 1) {
    (**(code **)(**(int **)(param_1 + 0x34) + 0x38))(*(int **)(param_1 + 0x34),0,local_28);
  }
  else {
    piVar1 = (int *)(param_1 + 0x30);
    if (((*piVar1 == 0) &&
        (iVar2 = (**(code **)(**(int **)(param_1 + 8) + 0x50))
                           (*(int **)(param_1 + 8),*(undefined4 *)(param_1 + 0xc),
                            *(undefined4 *)(param_1 + 0xc),*(undefined4 *)(param_1 + 0x1c),1,
                            *(undefined4 *)(param_1 + 0x10),0,piVar1), iVar2 < 0)) &&
       (iVar2 = (**(code **)(**(int **)(param_1 + 8) + 0x50))
                          (*(int **)(param_1 + 8),*(undefined4 *)(param_1 + 0xc),
                           *(undefined4 *)(param_1 + 0xc),*(undefined4 *)(param_1 + 0x1c),0,
                           *(undefined4 *)(param_1 + 0x10),0,piVar1), iVar2 < 0)) {
      return iVar2;
    }
    (**(code **)(*(int *)*piVar1 + 0x38))((int *)*piVar1,0,local_28);
  }
  *(uint *)(param_1 + 0x46c) = local_20 & 1;
  if ((local_20 & 1) == 0) {
    piVar1 = (int *)(param_1 + 0x20);
    if ((*piVar1 == 0) &&
       (iVar2 = (**(code **)(**(int **)(param_1 + 8) + 100))
                          (*(int **)(param_1 + 8),*(undefined4 *)(param_1 + 0xc),
                           *(undefined4 *)(param_1 + 0xc),*(undefined4 *)(param_1 + 0x10),0,1,piVar1
                          ), iVar2 < 0)) {
      return iVar2;
    }
    local_8 = (int *)*piVar1;
  }
  else if (*(int *)(param_1 + 0x460) == 1) {
    (**(code **)(**(int **)(param_1 + 0x34) + 0x3c))(*(int **)(param_1 + 0x34),param_2);
  }
  else {
    (**(code **)(**(int **)(param_1 + 0x30) + 0x3c))(*(int **)(param_1 + 0x30),0,&local_8);
  }
  piVar1 = (int *)(param_1 + 0x24);
  if (((*piVar1 == 0) && (*(int *)(param_1 + 0x14) != 0)) &&
     (iVar2 = (**(code **)(**(int **)(param_1 + 8) + 0x68))
                        (*(int **)(param_1 + 8),*(undefined4 *)(param_1 + 0xc),
                         *(undefined4 *)(param_1 + 0xc),*(undefined4 *)(param_1 + 0x18),0,piVar1),
     iVar2 < 0)) {
    return iVar2;
  }
  (**(code **)(**(int **)(param_1 + 8) + 0x7c))(*(int **)(param_1 + 8),local_8,*piVar1);
  (**(code **)(**(int **)(param_1 + 8) + 0xa0))(*(int **)(param_1 + 8),param_1 + 0x474);
  if (*(int *)(param_1 + 0x46c) != 0) {
    (**(code **)(*local_8 + 8))(local_8);
  }
  iVar2 = (**(code **)(**(int **)(param_1 + 8) + 0x88))(*(int **)(param_1 + 8));
  if (-1 < iVar2) {
    *(undefined4 *)(param_1 + 0x464) = param_2;
    *(undefined4 *)(param_1 + 0x468) = 1;
    iVar2 = 0;
  }
  return iVar2;
}

