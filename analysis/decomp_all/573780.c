
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

undefined4 FUN_00573780(int param_1,int param_2,int param_3,undefined4 param_4,int param_5)

{
  int iVar1;
  undefined4 *puVar2;
  char local_3028 [24];
  int local_3010;
  undefined1 local_300c;
  undefined4 local_300b;
  char local_200c;
  undefined4 local_200b;
  undefined4 local_100c;
  undefined1 *local_1008;
  char local_1004;
  undefined4 local_1003;
  undefined4 uStackY_24;
  char *pcStackY_20;
  int iStackY_1c;
  char *pcStackY_18;
  
  FUN_0056e230();
  local_300c = 0;
  puVar2 = &local_300b;
  for (iVar1 = 0x3ff; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0;
    puVar2 = puVar2 + 1;
  }
  *(undefined2 *)puVar2 = 0;
  *(undefined1 *)((int)puVar2 + 2) = 0;
  local_200c = '\0';
  puVar2 = &local_200b;
  for (iVar1 = 0x3ff; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0;
    puVar2 = puVar2 + 1;
  }
  *(undefined2 *)puVar2 = 0;
  *(undefined1 *)((int)puVar2 + 2) = 0;
  local_1004 = '\0';
  puVar2 = &local_1003;
  for (iVar1 = 0x3ff; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0;
    puVar2 = puVar2 + 1;
  }
  *(undefined2 *)puVar2 = 0;
  *(undefined1 *)((int)puVar2 + 2) = 0;
  local_1008 = &stack0x00000018;
  if ((param_1 < 0) || (2 < param_1)) {
    return 0xffffffff;
  }
  if ((param_1 == 2) && (iVar1 = (*API_KERNEL32_DLL_InterlockedIncrement)(), 0 < iVar1)) {
    if (DAT_0080a478 == (code *)0x0) {
      local_3010 = (*DAT_00592184)();
      if (local_3010 == 0) {
        return 0xffffffff;
      }
      pcStackY_18 = (char *)0x573848;
      DAT_0080a478 = (code *)(*DAT_005922cc)();
      if (DAT_0080a478 == (code *)0x0) {
        return 0xffffffff;
      }
    }
    pcStackY_18 = &local_200c;
    iStackY_1c = 0x573878;
    (*DAT_0080a478)();
    (*API_KERNEL32_DLL_OutputDebugStringA)();
    (*API_KERNEL32_DLL_InterlockedDecrement)();
    FUN_00573670();
    return 0xffffffff;
  }
  if (param_5 != 0) {
    pcStackY_18 = &local_1004;
    iStackY_1c = 0x5738c2;
    iVar1 = FUN_00572640();
    if (iVar1 < 0) {
      FUN_0056cd90();
    }
  }
  if (param_1 == 2) {
    FUN_0056cd90();
  }
  FUN_0056cda0();
  if (param_1 == 2) {
    if ((_UNK_00761b7c & 1) != 0) {
      FUN_0056cda0();
    }
    FUN_0056cda0();
  }
  if (param_2 == 0) {
    FUN_0056cd90();
  }
  else {
    pcStackY_18 = "%s(%d) : %s";
    iStackY_1c = 0x1000;
    pcStackY_20 = &local_200c;
    uStackY_24 = 0x573995;
    iVar1 = FUN_005715b0();
    if (iVar1 < 0) {
      FUN_0056cd90();
    }
  }
  if (DAT_0080bb64 != (code *)0x0) {
    pcStackY_18 = (char *)0x5739e9;
    iVar1 = (*DAT_0080bb64)();
    if (iVar1 != 0) {
      if (param_1 != 2) {
        return local_100c;
      }
      (*API_KERNEL32_DLL_InterlockedDecrement)();
      return local_100c;
    }
  }
  if (((*(uint *)(&DAT_00761b74 + param_1 * 4) & 1) != 0) &&
     (*(int *)(&DAT_00761b80 + param_1 * 4) != -1)) {
    pcStackY_18 = (char *)0x573a3f;
    _strlen(&local_200c);
    pcStackY_18 = &local_200c;
    iStackY_1c = *(int *)(&DAT_00761b80 + param_1 * 4);
    pcStackY_20 = (char *)0x573a5b;
    (*DAT_005922bc)();
  }
  if ((*(uint *)(&DAT_00761b74 + param_1 * 4) & 2) != 0) {
    (*API_KERNEL32_DLL_OutputDebugStringA)();
  }
  if ((*(uint *)(&DAT_00761b74 + param_1 * 4) & 4) != 0) {
    if (param_3 != 0) {
      pcStackY_18 = (char *)0x573aa2;
      __itoa(param_3,local_3028,10);
    }
    pcStackY_18 = (char *)param_2;
    iStackY_1c = param_1;
    pcStackY_20 = (char *)0x573ad6;
    local_100c = FUN_00573b10();
    if (param_1 != 2) {
      return local_100c;
    }
    (*API_KERNEL32_DLL_InterlockedDecrement)();
    return local_100c;
  }
  if (param_1 == 2) {
    (*API_KERNEL32_DLL_InterlockedDecrement)();
  }
  return 0;
}

