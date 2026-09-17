
void __thiscall
FUN__text__0042b980(int *param_1,undefined4 param_2,undefined4 param_3,undefined4 param_4,
                   undefined4 param_5)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_4c [16];
  int local_c;
  int *local_8;
  
  puVar2 = local_4c;
  for (iVar1 = 0x12; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  if ((*param_1 != 0) && (param_1[3] == 0)) {
    local_8 = param_1;
    (*API_COMCTL32_DLL_ImageList_BeginDrag)(*param_1,param_3,0,0);
    local_c = FUN__text__0056ce80();
    if (local_c == 1) {
      (*API_COMCTL32_DLL_ImageList_DragEnter)(param_2,param_4,param_5);
      local_c = FUN__text__0056ce80();
      local_8[3] = 1;
    }
  }
  local_8 = (int *)0x42ba20;
  FUN__text__0056ce80();
  return;
}

