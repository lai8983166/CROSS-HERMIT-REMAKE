
void __thiscall FUN__text__00413b10(int param_1,undefined4 param_2)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_4c [16];
  int local_c;
  int local_8;
  
  puVar2 = local_4c;
  for (iVar1 = 0x12; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  if ((((*(int *)(param_1 + 0xb20c) != 0) && (*(int *)(param_1 + 0xb278) != 0)) &&
      (*(int *)(param_1 + 0xb27c) != 0)) &&
     (local_8 = param_1, iVar1 = FUN__text__00413cf0(), iVar1 == 0)) {
    *(undefined4 *)(local_8 + 0xb250) = 0;
    *(undefined4 *)(local_8 + 0xb248) = 1;
    *(undefined4 *)(local_8 + 0xb234) = *(undefined4 *)(local_8 + 0xb224);
    *(undefined4 *)(local_8 + 0xb238) = *(undefined4 *)(local_8 + 0xb228);
    *(undefined4 *)(local_8 + 0xb23c) = *(undefined4 *)(local_8 + 0xb230);
    *(undefined4 *)(local_8 + 0xb240) = 1;
    *(undefined4 *)(local_8 + 0xb254) = 0;
    *(undefined4 *)(local_8 + 0xb258) = 0;
    _memset((void *)(local_8 + 0xb244),0,4);
    *(undefined4 *)(local_8 + 0xb24c) = param_2;
    *(undefined4 *)(local_8 + 0xb25c) = 0;
    *(undefined4 *)(local_8 + 0xb260) = 0;
    (**(code **)(**(int **)(local_8 + 0xb20c) + 0x3c))
              (*(undefined4 *)(local_8 + 0xb20c),0,*(undefined4 *)(local_8 + 0xb1f8),param_2,
               *(uint *)(local_8 + 0xb1fc) | 4,local_8 + 0xb234,local_8 + 0xb210);
    local_c = FUN__text__0056ce80();
    if ((-1 < local_c) && (iVar1 = FUN__text__00413fa0(), iVar1 == 0)) {
      FUN__text__0042b2d0("DISPLAYMODE:FULL:SCR(%d,%d,%d)\n",*(undefined4 *)(local_8 + 0xb224),
                          *(undefined4 *)(local_8 + 0xb228),*(undefined4 *)(local_8 + 0xb230));
    }
  }
  local_8 = 0x413cdd;
  FUN__text__0056ce80();
  return;
}

