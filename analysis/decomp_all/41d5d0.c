
void __fastcall FUN__text__0041d5d0(undefined4 *param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_4c [12];
  undefined4 uStack_1c;
  int local_c;
  undefined4 *local_8;
  
  puVar2 = local_4c;
  for (iVar1 = 0x12; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_8 = param_1;
  (*API_COMBASE_DLL_CoCreateInstance)(&DAT_005cfd7c,0,3,&DAT_005ce80c,param_1);
  local_c = FUN__text__0056ce80();
  if (-1 < local_c) {
    (*(code *)**(undefined4 **)*local_8)(*local_8,&DAT_005cef3c,local_8 + 1);
    local_c = FUN__text__0056ce80();
    if (-1 < local_c) {
      (*(code *)**(undefined4 **)*local_8)(*local_8,&DAT_005ce8dc,local_8 + 2);
      local_c = FUN__text__0056ce80();
      if (-1 < local_c) {
        (*(code *)**(undefined4 **)*local_8)(*local_8,&DAT_005cef0c,local_8 + 3);
        local_c = FUN__text__0056ce80();
        if (-1 < local_c) {
          (*(code *)**(undefined4 **)*local_8)(*local_8,&DAT_005cef1c,local_8 + 5);
          local_c = FUN__text__0056ce80();
          if (-1 < local_c) {
            (*(code *)**(undefined4 **)*local_8)(*local_8,&DAT_005ceefc,local_8 + 4);
            local_c = FUN__text__0056ce80();
            if (-1 < local_c) {
              (**(code **)(*(int *)local_8[5] + 0x34))(local_8[5],PTR_DAT_007a0bb4,0x464,local_8);
              local_c = FUN__text__0056ce80();
              if (-1 < local_c) goto LAB__text__0041d776;
            }
          }
        }
      }
    }
  }
  FUN__text__0041d040(local_c);
  FUN__text__0041d400();
LAB__text__0041d776:
  uStack_1c = 0x41d783;
  FUN__text__0056ce80();
  return;
}

