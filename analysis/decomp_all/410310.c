
void FUN__text__00410310(undefined4 param_1,undefined4 param_2,undefined4 param_3,undefined4 param_4
                        ,undefined2 param_5,undefined4 param_6,undefined1 param_7)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_4c [16];
  int local_c;
  undefined4 local_8;
  
  puVar2 = local_4c;
  for (iVar1 = 0x12; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  iVar1 = FUN__text__0040e2a0(param_1,param_2,param_3,param_4);
  if (iVar1 == 0) {
    local_c = FUN__text__0040dcd0(4);
    *(undefined4 *)(local_c + 4) = 4;
    *(undefined2 *)(local_c + 10) = (undefined2)param_1;
    *(undefined2 *)(local_c + 0xc) = (undefined2)param_2;
    *(undefined2 *)(local_c + 0xe) = (undefined2)param_3;
    *(undefined2 *)(local_c + 0x10) = (undefined2)param_4;
    *(undefined2 *)(local_c + 0x12) = param_5;
    *(undefined4 *)(local_c + 0x14) = param_6;
    *(undefined1 *)(local_c + 8) = param_7;
    FUN__text__0040df20(local_c,param_5);
  }
  local_8 = 0x4103dd;
  FUN__text__0056ce80();
  return;
}

