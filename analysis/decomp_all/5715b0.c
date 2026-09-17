
undefined4 FUN_005715b0(undefined1 *param_1,int param_2,int param_3)

{
  code *pcVar1;
  int iVar2;
  undefined4 uVar3;
  undefined1 *local_24;
  int local_20;
  undefined1 *local_1c;
  undefined4 local_18;
  
  if ((param_1 == (undefined1 *)0x0) &&
     (iVar2 = FUN_00573780(2,"sprintf.c",0x5d,0,"string != NULL"), iVar2 == 1)) {
    pcVar1 = (code *)swi(3);
    uVar3 = (*pcVar1)();
    return uVar3;
  }
  if ((param_3 == 0) && (iVar2 = FUN_00573780(2,"sprintf.c",0x5e,0,"format != NULL"), iVar2 == 1)) {
    pcVar1 = (code *)swi(3);
    uVar3 = (*pcVar1)();
    return uVar3;
  }
  local_18 = 0x42;
  local_1c = param_1;
  local_24 = param_1;
  local_20 = param_2;
  uVar3 = FUN_00575940(&local_24,param_3,&stack0x00000010);
  local_20 = local_20 + -1;
  if (local_20 < 0) {
    FUN_005756c0(0,&local_24);
  }
  else {
    *local_24 = 0;
  }
  return uVar3;
}

