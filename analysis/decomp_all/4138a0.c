
void __thiscall FUN__text__004138a0(int param_1,undefined4 param_2)

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
  if (*(int *)(param_1 + 0xb20c) != 0) {
    *(undefined4 *)(param_1 + 0xb204) = param_2;
    local_8 = param_1;
    (**(code **)(**(int **)(param_1 + 0xb20c) + 0x20))
              (*(undefined4 *)(param_1 + 0xb20c),0,param_1 + 0xb214);
    FUN__text__0056ce80();
    *(undefined4 *)(local_8 + 0xb250) = 1;
    *(undefined4 *)(local_8 + 0xb248) = 1;
    *(undefined4 *)(local_8 + 0xb234) = *(undefined4 *)(local_8 + 0xb278);
    *(undefined4 *)(local_8 + 0xb238) = *(undefined4 *)(local_8 + 0xb27c);
    *(undefined4 *)(local_8 + 0xb23c) = *(undefined4 *)(local_8 + 0xb220);
    *(undefined4 *)(local_8 + 0xb240) = 1;
    *(undefined4 *)(local_8 + 0xb254) = 0;
    *(undefined4 *)(local_8 + 0xb258) = 0;
    _memset((void *)(local_8 + 0xb244),0,4);
    *(undefined4 *)(local_8 + 0xb24c) = param_2;
    *(undefined4 *)(local_8 + 0xb25c) = 0;
    *(undefined4 *)(local_8 + 0xb260) = 0;
    *(undefined4 *)(local_8 + 0xb264) = 0;
    (**(code **)(**(int **)(local_8 + 0xb20c) + 0x3c))
              (*(undefined4 *)(local_8 + 0xb20c),0,*(undefined4 *)(local_8 + 0xb1f8),param_2,
               *(uint *)(local_8 + 0xb1fc) | 4,local_8 + 0xb234,local_8 + 0xb210);
    local_c = FUN__text__0056ce80();
    if ((-1 < local_c) && (iVar1 = FUN__text__00413fa0(), iVar1 == 0)) {
      _memset((void *)(local_8 + 0xba08),0,0x18);
      *(undefined4 *)(local_8 + 0xba08) = 0;
      *(undefined4 *)(local_8 + 0xba0c) = 0;
      *(undefined4 *)(local_8 + 0xba10) = *(undefined4 *)(local_8 + 0xb278);
      *(undefined4 *)(local_8 + 0xba14) = *(undefined4 *)(local_8 + 0xb27c);
      *(undefined4 *)(local_8 + 0xba18) = 0;
      *(undefined4 *)(local_8 + 0xba1c) = 0x3f800000;
      (**(code **)(**(int **)(local_8 + 0xb210) + 0xa0))
                (*(undefined4 *)(local_8 + 0xb210),local_8 + 0xba08);
      local_c = FUN__text__0056ce80();
    }
  }
  local_8 = 0x413afd;
  FUN__text__0056ce80();
  return;
}

