
void __thiscall
FUN__text__00416540(int param_1,int param_2,undefined4 param_3,undefined4 param_4,undefined2 param_5
                   ,undefined4 param_6,undefined4 param_7)

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
  if (((*(short *)(param_1 + 0xb28e) != 0) && (param_2 != 0)) &&
     (local_8 = param_1, iVar1 = FUN__text__0040e2a0(param_3,param_4,0x200,0x80), iVar1 == 0)) {
    local_c = FUN__text__0040dcd0(2);
    *(undefined4 *)(local_c + 4) = 2;
    *(int *)(local_c + 8) = param_2;
    *(undefined4 *)(local_c + 0x10) = param_7;
    *(undefined2 *)(local_c + 0xc) = (undefined2)param_3;
    *(undefined2 *)(local_c + 0xe) = (undefined2)param_4;
    (*API_KERNEL32_DLL_lstrcpyA)(local_c + 0x14,param_6);
    FUN__text__0056ce80();
    FUN__text__0040df20(local_c,param_5);
  }
  local_8 = 0x416636;
  FUN__text__0056ce80();
  return;
}

