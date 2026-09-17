
void __thiscall
FUN__text__0042bb90(int *param_1,undefined4 param_2,undefined4 param_3,undefined4 param_4)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_50 [16];
  undefined4 local_10;
  int local_c;
  int *local_8;
  
  puVar2 = local_50;
  for (iVar1 = 0x13; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  if ((*param_1 != 0) && (param_1[3] == 2)) {
    local_8 = param_1;
    (*API_COMCTL32_DLL_ImageList_GetDragImage)(0,0);
    local_c = FUN__text__0056ce80();
    if (local_c != 0) {
      local_10 = FUN__text__0042b870(param_2,param_3,param_4,0,0);
    }
  }
  local_8 = (int *)0x42bc19;
  FUN__text__0056ce80();
  return;
}

